# -*- coding: utf-8 -*-
#
# Copyright (c) 2019~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import inspect
import typing
import functools

import click

from .injectors import Injector, find, ensure, TYPE_INJECTOR_MAP
from .snake_case import convert as sc_convert
from .types import flag

_KEY_ATTRS = '__click_anno_attrs'

def attrs(**kwargs):
    '''
    append attrs to command or group like:

    ``` py
    @click_app
    @attrs(...)
    class ...
    ```

    attrs will pass into `click` module.
    '''
    def wrapper(type_or_func):
        setattr(type_or_func, _KEY_ATTRS, dict(kwargs))
        return type_or_func
    return wrapper


_UNSET = object()


class ArgumentAdapter:
    @classmethod
    def from_parameter(cls, param: inspect.Parameter):
        default = _UNSET if param.default is inspect.Parameter.empty else param.default
        annotation = _UNSET if param.annotation is inspect.Parameter.empty else param.annotation
        adapter = cls(param.name, param.kind, default, annotation)
        return adapter

    @classmethod
    def from_callable(cls, func) -> list:
        sign = inspect.signature(func)
        return [cls.from_parameter(param) for param in sign.parameters.values()]

    def __init__(self, param_name: str, param_kind: inspect._ParameterKind, param_def, param_anno):
        self._parameter_name: str = param_name # this name use for pass to the function
        self._parameter_key: str = param_name.strip('_') # this key use for get value from click args
        self._parameter_annotation = param_anno
        self._parameter_kind: inspect._ParameterKind = param_kind
        self._parameter_default = param_def

        self._click_decorator_name: str = None
        self._click_decorator_decls: list = []
        self._click_decorator_attrs: dict = {}
        self._injector: Injector = None

        anno = TYPE_INJECTOR_MAP.get(self._parameter_annotation, self._parameter_annotation)
        if isinstance(anno, Injector):
            self._injector = anno
        else:
            self._init_click_attrs()

    def _init_click_attrs(self):
        kind = self._parameter_kind
        annotation = self._parameter_annotation
        default = self._parameter_default

        self._click_decorator_decls: list = []
        self._click_decorator_attrs: dict = {}

        if kind is inspect.Parameter.POSITIONAL_OR_KEYWORD:
            if annotation is not _UNSET:
                if annotation is tuple:
                    self._click_decorator_attrs.setdefault('nargs', -1)

        elif kind is inspect.Parameter.VAR_POSITIONAL:
            self._click_decorator_attrs.setdefault('nargs', -1)

        elif kind is inspect.Parameter.KEYWORD_ONLY:
            self._click_decorator_name = 'option'
            self._click_decorator_attrs['required'] = True

        elif kind is inspect.Parameter.VAR_KEYWORD:
            raise RuntimeError('does not support var keyword parameters.')

        else:
            raise NotImplementedError

        if annotation is not _UNSET:
            if annotation is tuple:
                self._click_decorator_attrs.setdefault('nargs', -1)

            elif annotation is flag:
                self._click_decorator_name = 'option'
                self._click_decorator_attrs['is_flag'] = True

            elif isinstance(annotation, typing._GenericAlias):
                if annotation.__origin__ is tuple:
                    args = annotation.__args__
                    if kind is inspect.Parameter.VAR_POSITIONAL:
                        if len(args) == 2 and args[1] is Ellipsis:
                            self._click_decorator_attrs['type'] = args[0]
                        else:
                            raise ValueError(\
                                f'annotation of parameter {self._parameter_name} must be tuple or typing.Tuple[?, ...]')
                    else:
                        if any(x is not args[0] for x in args):
                            raise ValueError(\
                                f'annotation of parameter {self._parameter_name} must be same types')
                        else:
                            self._click_decorator_attrs.setdefault('nargs', len(args))
                            self._click_decorator_attrs['type'] = args[0]
                else:
                    raise ValueError('generic type must be typing.Tuple')
            else:
                self._click_decorator_attrs.setdefault('type', annotation)

        if self._click_decorator_name is None:
            if default is _UNSET:
                self._click_decorator_name = 'argument'
            else:
                self._click_decorator_name = 'option'

        if default is not _UNSET:
            if default is not None:
                self._click_decorator_attrs.setdefault('type', type(default))
            self._click_decorator_attrs['default'] = default
            self._click_decorator_attrs['show_default'] = True

        if self._click_decorator_name == 'option':
            self._click_decorator_decls.append('--' + self._parameter_key.replace('_', '-'))
        self._click_decorator_decls.append(self._parameter_key)

        assert self._click_decorator_name in ('argument', 'option')

    def get_click_decorator(self):
        if self._click_decorator_name:
            decorator =  getattr(click, self._click_decorator_name)
            return decorator(*self._click_decorator_decls, **self._click_decorator_attrs)

    def convert(self, args, kwargs, to_args: list, to_kwargs: dict):
        assert not args

        if self._injector:
            val = self._injector.get_value()
        else:
            val = kwargs.pop(self._parameter_key)

        if self._parameter_kind is inspect.Parameter.POSITIONAL_OR_KEYWORD:
            to_args.append(val)
        elif self._parameter_kind is inspect.Parameter.VAR_POSITIONAL:
            to_args.extend(val)
        else:
            to_kwargs[self._parameter_name] = val


class CallableAdapter:
    @classmethod
    def from_func(cls, func):
        adapter = cls(func)
        adapter.args_adapters.extend(ArgumentAdapter.from_callable(func))
        return adapter

    def __init__(self, func):
        self._func = func
        self.args_adapters = []

        # clone func info
        self.__name__ = func.__name__
        self.__doc__ = func.__doc__

    def __call__(self, *args, **kwargs):
        to_args = []
        to_kwargs = {}
        for adapter in self.args_adapters:
            adapter.convert(args, kwargs, to_args, to_kwargs)
        return self._func(*to_args, **to_kwargs)

    def get_wrapped_func(self):
        func = self
        for adapter in reversed(self.args_adapters):
            decorator = adapter.get_click_decorator()
            if decorator:
                func = decorator(func)
        return func


def command(func) -> click.Command:
    '''
    build a `function` as a `click.Command`.
    '''
    wrapped_func = CallableAdapter.from_func(func).get_wrapped_func()
    attrs = getattr(func, _KEY_ATTRS, {})
    return click.command(**attrs)(wrapped_func)


def create_init_wrapper(cls):
    @functools.wraps(cls)
    def init_wrapper(*args, **kwargs):
        ctx = click.get_current_context()
        ctx.__instance = cls(*args, **kwargs)
    return init_wrapper

def create_method_wrapper(func):
    @functools.wraps(func)
    def method_wrapper(*args, **kwargs):
        ctx = click.get_current_context()
        instance = ctx.parent.__instance
        return func(instance, *args, **kwargs)
    return method_wrapper


class GroupBuilderOptions:
    allow_inherit = False

    def group_name_format(self, command, name):
        return sc_convert(name).replace('_', '-')

    def command_name_format(self, command, name):
        return name.lower().replace('_', '-')


class GroupBuilder:

    def __init__(self, group, options: GroupBuilderOptions):
        self.group = group
        self.command_name_map = {}
        self.options = options

    def add_group(self, func, attrs):
        return self.group.group(**attrs)(func)

    def add_command(self, func, attrs):
        return self.group.command(**attrs)(func)

    def prepare_attrs(self, cmd, *, name, format_func):
        attrs: dict = getattr(cmd, _KEY_ATTRS, {}).copy()
        cmd_name = format_func(cmd, name)
        if cmd in self.command_name_map:
            # this is alias
            def_cmd_name = self.command_name_map[cmd]
            # alias should not use name from `attrs`, so we overwrite it.
            attrs['name'] = cmd_name
            attrs['help'] = f'alias of command ({def_cmd_name})'
        else:
            attrs.setdefault('name', cmd_name)
        self.command_name_map[cmd] = attrs['name']
        return attrs

    def make_command(self, cmd, *, name):
        attrs = self.prepare_attrs(cmd, name=name, format_func=self.options.command_name_format)

        adapter = CallableAdapter(create_method_wrapper(cmd))
        adapter.args_adapters.extend(ArgumentAdapter.from_callable(cmd))
        adapter.args_adapters.pop(0) # remove arg `self`
        self.add_command(adapter.get_wrapped_func(), attrs)

    def make_group(self, cls, *, name):
        attrs = self.prepare_attrs(cls, name=name, format_func=self.options.group_name_format)

        func = create_init_wrapper(cls)
        adapter = CallableAdapter(func)
        adapter.args_adapters.extend(ArgumentAdapter.from_callable(cls))
        group = self.add_group(adapter.get_wrapped_func(), attrs)

        group_builder = GroupBuilder(group, self.options)

        if self.options.allow_inherit:
            iter_subcommands = self.iter_subcommands_allow_inherit(cls)
        else:
            iter_subcommands = self.iter_subcommands_not_inherit(cls)

        for name, sub_cmd in iter_subcommands:
            if isinstance(sub_cmd, type):
                group_builder.make_group(sub_cmd, name=name)
            elif callable(sub_cmd):
                group_builder.make_command(sub_cmd, name=name)

        return group

    def iter_subcommands_not_inherit(self, cls):
        for name, sub_cmd in vars(cls).items():
            if name[:1] != '_':
                yield name, sub_cmd

    def iter_subcommands_allow_inherit(self, cls):
        for name in dir(cls):
            if name[:1] != '_':
                yield name, getattr(cls, name)


def click_app(cls: type = None, **kwargs) -> click.Group:
    '''
    build a `class` as a `click.Group`.

    use `kwargs` to override members of `GroupBuilderOptions`.
    '''

    def warpper(cls):
        options = GroupBuilderOptions()
        vars(options).update(kwargs)
        group_builder = GroupBuilder(click, options)
        return group_builder.make_group(cls, name=cls.__name__)

    return warpper(cls) if cls else warpper
