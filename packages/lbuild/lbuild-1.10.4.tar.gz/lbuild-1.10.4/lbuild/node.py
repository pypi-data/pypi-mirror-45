#!/usr/bin/env python3
#
# Copyright (c) 2015-2018, Fabian Greif
# Copyright (c) 2018, Niklas Hauser
# All Rights Reserved.
#
# The file is part of the lbuild project and is released under the
# 2-clause BSD license. See the file `LICENSE.txt` for the full license
# governing this code.

import os
import enum
import logging
import itertools

import anytree

import lbuild.filter
import lbuild.format
import lbuild.utils

from .exception import LbuildException, LbuildValidateException

LOGGER = logging.getLogger('lbuild.node')


def load_functions_from_file(repository, filename: str, required, optional=None, local=None):
    try:
        localpath = os.path.dirname(os.path.realpath(filename))

        if local is None:
            local = {}

        local.update({
            'localpath': RelocatePath(localpath),
            'repopath': RelocatePath(repository._filepath),
            'listify': lbuild.utils.listify,
            'listrify': lbuild.utils.listrify,

            'FileReader': LocalFileReaderFactory(localpath),
            'ValidateException': LbuildValidateException,
            'Module': lbuild.module.ModuleBase,

            'Query': lbuild.query.Query,
            'EnvironmentQuery': lbuild.query.EnvironmentQuery,

            'StringCollector': lbuild.collector.StringCollector,
            'PathCollector': lbuild.collector.PathCollector,
            'BooleanCollector': lbuild.collector.BooleanCollector,
            'NumericCollector': lbuild.collector.NumericCollector,
            'EnumerationCollector': lbuild.collector.EnumerationCollector,
            'CallableCollector': lbuild.collector.CallableCollector,

            'StringOption': lbuild.option.StringOption,
            'PathOption': lbuild.option.PathOption,
            'BooleanOption': lbuild.option.BooleanOption,
            'NumericOption': lbuild.option.NumericOption,
            'EnumerationOption': lbuild.option.EnumerationOption,
            'SetOption': lbuild.option.SetOption,
        })

        # LOGGER.debug("Parse filename '%s'", filename)
        local = lbuild.utils.with_forward_exception(
            repository,
            lambda: lbuild.utils.load_module_from_file(filename, local))
        functions = lbuild.utils.get_global_functions(local, required, optional)
        return functions

    except FileNotFoundError as error:
        raise LbuildException("Repository configuration file not found '{}'.".format(filename))

    except KeyError as error:
        raise LbuildException("Invalid repository configuration file '{}':\n"
                              " {}: {}".format(filename,
                                               error.__class__.__name__,
                                               error))


class RelocatePath:

    def __init__(self, basepath):
        self.basepath = basepath

    def __call__(self, *args):
        return os.path.join(self.basepath, *args)


class LocalFileReader:

    def __init__(self, basepath, filename):
        self.basepath = basepath
        self.filename = filename
        self._content = None

    def __str__(self):
        return self.read()

    def read(self):
        if self._content is None:
            with open(os.path.join(self.basepath, self.filename), encoding="utf-8") as file:
                self._content = file.read()
        return self._content


class LocalFileReaderFactory:

    def __init__(self, basepath):
        self.basepath = basepath

    def __call__(self, filename):
        return LocalFileReader(self.basepath, filename)


class NameResolver:
    """
    Name resolver for node.
    """

    def __init__(self, node, nodetype, selected=True, returner=None, defaulter=None):
        self._node = node
        self._type = nodetype
        self._str = nodetype.name.lower()
        self._returner = (lambda n: n) if returner is None else returner
        self._defaulter = (lambda n: n) if defaulter is None else defaulter
        self._selected = selected

    def get_node(self, key, check_dependencies=False):
        node = self._node._resolve_partial_max(key, max_results=1)[0]
        if not node._available:
            raise LbuildException("{} '{}' is not available!".format(self._str, node.fullname))

        if self._selected and not node._selected:
            raise LbuildException("{} '{}' is not selected!".format(self._str, node.fullname))

        if node._type != self._type:
            raise LbuildException("'{}' is of type '{}', but searching for '{}'!"
                                  .format(node.fullname, node._type.name.lower(), self._str))

        if check_dependencies and node.type in {BaseNode.Type.OPTION, BaseNode.Type.QUERY, BaseNode.Type.COLLECTOR}:
            if node.parent != self._node:
                if all(n.type not in {BaseNode.Type.PARSER, BaseNode.Type.REPOSITORY} for n in {self._node, node.module}):
                    if node.parent not in self._node.dependencies:
                        if self._selected or node.type not in {BaseNode.Type.COLLECTOR}:
                            LOGGER.warning("Module '{}' accessing '{}' without depending on '{}'!"
                                           .format(self._node.fullname, node.fullname, node.module.fullname))

        return node

    def __getitem__(self, key: str):
        node = self.get_node(key, check_dependencies=True)
        return self._returner(node)

    def get(self, key, default=None):
        try:
            node = self.get_node(key)
            return self._returner(node)
        except LbuildException:
            return self._defaulter(default)

    def __contains__(self, key):
        try:
            _ = self.get_node(key)
            return True
        except LbuildException:
            return False

    def __len__(self):
        return len(self._node._findall(self._type, selected=self._selected))

    def __repr__(self):
        return repr(self._node._findall(self._type, selected=self._selected))


class BaseNode(anytree.Node):
    separator = ":"
    resolver = anytree.Resolver()

    @enum.unique
    class Type(enum.IntEnum):
        """This order is used to sort the children for the tree view"""
        PARSER = 1
        REPOSITORY = 2
        OPTION = 3
        CONFIG = 4
        QUERY = 5
        COLLECTOR = 6
        MODULE = 7

    def __init__(self, name, node_type, repository=None):
        anytree.Node.__init__(self, name)
        if self.separator in str(name):
            raise LbuildException("Path separator ':' is not allowed in '{}({})' name!"
                                  .format(self.__class__.__name__, self.name))
        self._type = node_type
        self._functions = {}

        self._fullname = name
        self._filename = None

        # Dependency management
        self._repository = repository
        self._dependency_module_names = []
        self._dependencies_resolved = False
        self._dependencies = []

        self._description = ""
        # All _update()-able traits: defaults
        self._available_default = True
        self._selected_default = True
        self._format_description_default = lbuild.format.format_description
        self._format_short_description_default = lbuild.format.format_short_description

        # All _update()-able traits: defaults
        self._available = (self._type != BaseNode.Type.MODULE)
        self._selected = True
        self._format_description = self._format_description_default
        self._format_short_description = self._format_short_description_default
        self._ignore_patterns = lbuild.utils.DEFAULT_IGNORE_PATTERNS
        self._filters = lbuild.filter.DEFAULT_FILTERS

    @property
    def format_description(self):
        return lbuild.format.format_description

    @property
    def format_short_description(self):
        return lbuild.format.format_short_description

    @property
    def _filepath(self):
        return os.path.dirname(self._filename)

    @property
    def fullname(self):
        if self._fullname is None:
            self._fullname = self.name
        return self._fullname

    @property
    def description_name(self):
        return self.fullname

    @property
    def class_name(self):
        return self.__class__.__name__

    @property
    def type(self):
        return self._type

    @property
    def queries(self):
        return self.all_queries(depth=2)

    @property
    def options(self):
        return self.all_options(depth=2)

    @property
    def submodules(self):
        return self.all_modules(depth=2)

    @property
    def configurations(self):
        return self._findall(self.Type.CONFIG, depth=2)

    @property
    def collectors(self):
        return self._findall(self.Type.COLLECTOR, depth=2)

    @property
    def repository(self):
        return self._repository

    @property
    def dependencies(self):
        self._resolve_dependencies()
        return self._dependencies + [d for o in self.options
                                     for d in o._dependencies
                                     if d != self]

    @property
    def description(self):
        return self._format_description(self, str(self._description))

    @property
    def short_description(self):
        return self._format_short_description(self, str(self._description))

    @description.setter
    def description(self, description):
        self._description = "" if description is None else description

    @property
    def option_value_resolver(self):
        return NameResolver(self, self.Type.OPTION,
                            returner=lambda n: n.value)

    @property
    def option_resolver(self):
        return NameResolver(self, self.Type.OPTION)

    def query_resolver(self, env):
        return NameResolver(self, self.Type.QUERY,
                            returner=lambda n: n.value(env))

    @property
    def collector_resolver(self):
        return NameResolver(self, self.Type.COLLECTOR)

    @property
    def collector_values_resolver(self):
        return NameResolver(self, self.Type.COLLECTOR,
                            returner=lambda n: n.values(),
                            defaulter=lbuild.utils.listify)

    @property
    def collector_available_resolver(self):
        return NameResolver(self, self.Type.COLLECTOR, selected=False)

    @property
    def module_resolver(self):
        return NameResolver(self, self.Type.MODULE)

    def render(self, filterfunc=None):
        return lbuild.format.format_node_tree(self, filterfunc)

    def add_dependencies(self, *dependencies):
        """
        Add a new dependencies.

        The module name has not to be fully qualified.
        """
        self._dependency_module_names += dependencies

    def add_child(self, node):
        if node.name in [child.name for child in self.children]:
            raise LbuildException("{} name '{}' is already defined in Module '{}'!"
                                  .format(node.__class__.__name__, node.name, self.fullname))
        node._repository = self._repository
        node.parent = self
        node.add_dependencies(self.fullname)
        node._fullname = self.fullname + ":" + node.name

    def all_queries(self, depth=None, selected=True):
        return self._findall(self.Type.QUERY, depth, selected)

    def all_options(self, depth=None, selected=True):
        return self._findall(self.Type.OPTION, depth, selected)

    def all_modules(self, depth=None, selected=True):
        return self._findall(self.Type.MODULE, depth, selected)

    def _findall(self, node_type, depth=None, selected=True):

        def _filter(node):
            return (node._type == node_type and
                    node._available and
                    (node._selected or not selected) and
                    node is not self)

        return anytree.search.findall(self, maxlevel=depth, filter_=_filter)

    def _resolve_dependencies(self, ignore_failure=False):
        """
        Update the internal list of dependencies.

        Resolves the module names to the actual module objects.
        """
        if self._dependencies_resolved:
            return
        dependencies = set()
        # print(self.fullname, self._dependency_module_names)
        dependency_names = set(n for n in self._dependency_module_names if ":" in n)
        for dependency_name in dependency_names:
            try:
                dependencies.add(self.module_resolver[dependency_name])
            except LbuildException as error:
                if not ignore_failure:
                    raise LbuildException("Cannot resolve dependencies!\n{}".format(error))
                LOGGER.debug("ignoring %s", dependency_name)
        self._dependencies = list(dependencies)
        self._dependencies_resolved = not ignore_failure
        for child in self.children:
            child._resolve_dependencies(ignore_failure)

    def _resolve_partial_max(self, query, max_results=1):
        nodes = self._resolve_partial(query, None)
        if nodes is None:
            raise LbuildException("Unknown '{}' in module '{}'!".format(query, self.fullname))
        if len(nodes) > max_results:
            raise LbuildException("Ambiguous '{}'! Found: '{}'"
                                  .format(query,
                                          "', '".join([n.fullname for n in nodes])))
        return nodes

    def _resolve_partial(self, query, default):
        # Try if query result is unique
        resolved1 = self._resolve(query, [])
        if len(resolved1) == 1:
            return resolved1

        # no result or ambiguous? try to fill the partial name
        query = ":".join(self._fill_partial_name(["" if p == "*" else p for p in query.split(":")]))
        resolved2 = self._resolve(query, [])

        if not (resolved2 or resolved1):
            # neither found anything
            return default
        if not resolved2:
            return resolved1
        if not resolved1:
            return resolved2

        # return the less ambiguous one
        return resolved2 if len(resolved2) < len(resolved1) else resolved1

    def _resolve(self, query, default):
        # :*   -> non-recursive
        # :**  -> recursive
        query = ":".join(p if p else "*" for p in query.strip().split(":"))
        try:
            qquery = ":" + query.replace(":**", "")
            if self.root._type == self.Type.PARSER:
                qquery = ":lbuild" + qquery
            found_modules = BaseNode.resolver.glob(self.root, qquery)
        except (anytree.resolver.ChildResolverError, anytree.resolver.ResolverError):
            return default

        modules = found_modules
        if query.endswith(":**"):
            for module in found_modules:
                modules.extend(module.descendants)

        return modules if modules else default

    def _fill_partial_name(self, partial_name):
        """
        Fill the array of the module name with the parts of the full name
        of the current module.

        Returns an array of the full name.
        """
        module_fullname_parts = self.fullname.split(":")

        # if partial_name is just leaf name, set scope to local node
        if len(partial_name) == 1:
            partial_name = module_fullname_parts + partial_name
        # Limit length of the module name to the length of the requested name
        depth = len(partial_name)
        if len(module_fullname_parts) > depth:
            module_fullname_parts = module_fullname_parts[:depth]

        # Using zip_longest restricts the name to the length of full name
        # if it is shorted than the requested module name.
        name = []
        for part, fill in itertools.zip_longest(partial_name,
                                                module_fullname_parts,
                                                fillvalue=""):
            name.append(fill if (part == "") else part)
        return name

    def _update_attribute(self, attr):
        self_attr = getattr(self, attr, "unknown")
        parent_attr = getattr(self.parent, attr, "unknown")
        if self_attr == "unknown" or parent_attr == "unknown":
            raise LbuildException("Cannot update non-existant attribute '{}'!".format(attr))

        if isinstance(self_attr, list):
            self_attr = list(set(self_attr + parent_attr))
            return
        if isinstance(self_attr, dict):
            self_attr.update(parent_attr)
            return

        default = getattr(self, attr + "_default")
        if (parent_attr != default) and (self_attr == default):
            setattr(self, attr, parent_attr)

    def _update_format(self):
        if self.parent:
            self._update_attribute("_format_description")
            self._update_attribute("_format_short_description")

        for child in self.children:
            child._update_format()

    def _update(self):
        if self.parent:
            self._update_attribute("_format_description")
            self._update_attribute("_format_short_description")
            self._update_attribute("_available")
            self._update_attribute("_selected")
            self._update_attribute("_ignore_patterns")
            self._update_attribute("_filters")

        for child in self.children:
            child._update()

    def _relocate_relative_path(self, path):
        """
        Relocate relative paths to the path of the repository
        configuration file.
        """
        if not os.path.isabs(path):
            path = os.path.join(self._filepath, path)
        return os.path.normpath(path)
