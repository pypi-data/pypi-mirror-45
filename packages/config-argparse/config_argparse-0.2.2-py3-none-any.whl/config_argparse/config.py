from __future__ import annotations

from typing import Callable, List, Set, Tuple, Type, Any, MutableMapping, Mapping, cast
import argparse
import copy
from .argparse_action import NoOpAction
from .value import Value


class Config(MutableMapping[str, Any]):
    def __init__(self, defaults=None):
        self._copy_class_variables(self)
        self._defaults = defaults

    def _new(self):
        namespace = type(self)()
        if self._defaults:
            defaults = copy.deepcopy(self._defaults)
            self._assign_values(defaults, namespace)
        return namespace

    def parse_known_args(
            self,
            args: List[str] = None,
            prefix='',
            namespace: MutableMapping[str, Any] = None,
    ) -> Tuple[MutableMapping[str, Any], List[str]]:
        if args is None:
            args = []
        if namespace is None:
            namespace = self._new()

        def is_name(s):
            return s.startswith('--')

        left_args: Set[str] = set(filter(is_name, args))
        parser = argparse.ArgumentParser(self.__class__.__name__, allow_abbrev=False)
        self._add_arguments(parser, prefix, namespace)
        if '--' + prefix + 'help' in args:
            parser.print_help()
            parser.exit()
        _, left = parser.parse_known_args(args, namespace=namespace)
        left_args = left_args & set(filter(is_name, left))
        left_args = left_args & self._parse_config(args, prefix, namespace)

        return namespace, list(left_args)

    def parse_args(self, *args, **kwards) -> MutableMapping[str, Any]:
        namespace, left_args = self.parse_known_args(*args, **kwards)
        if len(left_args) > 0:
            raise Exception('unknown arguments: {}'.format(left_args))
        return namespace

    def todict(self):
        res = {}
        for class_variable in self:
            if isinstance(self[class_variable], Config):
                res[class_variable] = self[class_variable].todict()
            else:
                res[class_variable] = self[class_variable]
        return res

    def _add_arguments(
            self,
            parser: argparse._ActionsContainer,
            prefix: str,
            namespace: MutableMapping[str, Any],
    ):
        for class_variable in self:
            name = '--' + prefix + class_variable
            value = self[class_variable]
            if isinstance(value, Config):
                parser.add_argument(name, action=NoOpAction, dest=class_variable)
            elif isinstance(value, DynamicConfig):
                parser.add_argument(name, action=NoOpAction, dest=class_variable)
            elif isinstance(value, Value):
                value.add_argument(parser, name, class_variable)
            else:
                Value(value).add_argument(parser, name, class_variable)

            if isinstance(namespace.get(class_variable, None), Value):
                namespace[class_variable] = namespace[class_variable].default

    def _parse_config(
            self,
            args: List[str],
            prefix: str,
            namespace: MutableMapping[str, Any],
    ) -> Set[str]:
        left = set(filter(lambda s: s.startswith('--'), args))
        for class_variable in self:
            dest = prefix + class_variable
            name = '--' + dest
            val = self[class_variable]

            if isinstance(val, Config):
                sub_namespace = namespace.get(class_variable, None)
                sub_namespace, l = val.parse_known_args(
                    args,
                    prefix=dest + '.',
                    namespace=sub_namespace,
                )
                namespace[class_variable] = sub_namespace
                left = left & set(l)
            elif isinstance(val, DynamicConfig):
                sub_namespace = namespace.get(class_variable, None)
                if isinstance(sub_namespace, DynamicConfig):
                    sub_namespace = None
                sub_namespace, l, _ = val.parse_args(
                    namespace,
                    args,
                    prefix=dest + '.',
                    namespace=sub_namespace,
                )
                namespace[class_variable] = sub_namespace
                left = left & set(l)
        return left

    def _assign_values(self, src: Mapping[str, Any], dest: MutableMapping[str, Any]):
        for class_variable in self:
            if class_variable in src:
                if isinstance(dest[class_variable], Config):
                    if not hasattr(src[class_variable], '__iter__'):
                        raise Exception('default value of {} in {} should be iterable'.format(class_variable, src))
                    dest[class_variable]._assign_values(src[class_variable], dest[class_variable])
                else:
                    dest[class_variable] = src[class_variable]

    def __repr__(self):
        res = ['{}:'.format(self.__class__.__name__)]
        for class_variable in self:
            txt = str(self[class_variable]).replace('\n', '\n\t')
            res.append('\t{} = {}'.format(class_variable, txt))
        return '\n'.join(res)

    def __getitem__(self, key):
        if not self.is_class_variable(key):
            raise KeyError
        return getattr(self, key)

    def __setitem__(self, key, value):
        if not self.is_class_variable(key):
            raise KeyError
        setattr(self, key, value)

    def __delitem__(self, key):
        delattr(self, key)

    def __iter__(self):
        for key in filter(self.is_class_variable, self.__dict__):
            yield key

    def __len__(self):
        # TODO: computational complexity
        return len(filter(self.is_class_variable, self.__dict__))

    @classmethod
    def is_class_variable(cls, name: str) -> bool:
        return hasattr(cls, name) and not name.startswith('_') and not callable(getattr(cls, name))

    @classmethod
    def _copy_class_variables(cls, cls_instance):
        ''' assign instance variables by copying all class variables to instance '''
        # may be overwritten by child
        for base in filter(lambda c: issubclass(c, Config), cls.__bases__):
            base._copy_class_variables(cls_instance)

        for class_variable in filter(cls.is_class_variable, vars(cls)):
            val = getattr(cls, class_variable)
            setattr(cls_instance, class_variable, copy.deepcopy(val))


class DynamicConfig:
    def __init__(self, config_factory: Callable[[MutableMapping[str, Any]], Config]):
        self.config_factory = config_factory

    def parse_args(
            self,
            parent_config: MutableMapping[str, Any],
            args: List[str],
            prefix: str,
            namespace: MutableMapping[str, Any],
    ) -> Tuple[MutableMapping[str, Any], List[str], Config]:
        config: Config = self.config_factory(parent_config)
        if not isinstance(config, Config):
            raise Exception('DynamicConfig: config_factory should return instance of Config, but returned {}'.format(config))
        namespace, left_args = config.parse_known_args(args, prefix, namespace=namespace)
        return namespace, left_args, config
