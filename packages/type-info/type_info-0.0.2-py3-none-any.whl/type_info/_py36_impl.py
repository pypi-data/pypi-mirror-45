# -*- coding: utf-8 -*-
#
# Copyright (c) 2019~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import sys
import typing
import collections
import collections.abc
import contextlib

from ._core import (
    STD_TYPES,
    TypeInfo, TypeVarTypeInfo, GenericTypeInfo,
    from_any, from_type, from_union,
)

_GENERICALIAS_GENERIC_DYNAMIC_MAP = {
    typing.Dict: dict,
    typing.FrozenSet: frozenset,
    typing.List: list,
    typing.Set: set,
    typing.Tuple: tuple,

    # collections
    typing.ChainMap: collections.ChainMap,
    typing.Counter: collections.Counter,
    typing.DefaultDict: collections.defaultdict,
    typing.Deque: collections.deque,

    # collections.abc
    typing.AsyncGenerator: collections.abc.AsyncGenerator,
    typing.AsyncIterable: collections.abc.AsyncIterable,
    typing.AsyncIterator: collections.abc.AsyncIterator,
    typing.Awaitable: collections.abc.Awaitable,
    typing.ByteString: collections.abc.ByteString,
    typing.Collection: collections.abc.Collection,
    typing.Container: collections.abc.Container,
    typing.Coroutine: collections.abc.Coroutine,
    typing.Generator: collections.abc.Generator,
    typing.Hashable: collections.abc.Hashable,
    typing.ItemsView: collections.abc.ItemsView,
    typing.Iterable: collections.abc.Iterable,
    typing.Iterator: collections.abc.Iterator,
    typing.KeysView: collections.abc.KeysView,
    typing.Mapping: collections.abc.Mapping,
    typing.MappingView: collections.abc.MappingView,
    typing.MutableMapping: collections.abc.MutableMapping,
    typing.MutableSequence: collections.abc.MutableSequence,
    typing.MutableSet: collections.abc.MutableSet,
    typing.Reversible: collections.abc.Reversible,
    typing.Sequence: collections.abc.Sequence,
    typing.AbstractSet: collections.abc.Set,
    typing.Sized: collections.abc.Sized,
    typing.ValuesView: collections.abc.ValuesView,
    typing.Callable: collections.abc.Callable,

    # contextlib
    typing.ContextManager: contextlib.AbstractContextManager,
}

def get_type_info(target):
    if target is typing.Any:
        return from_any()

    if isinstance(target, (typing.GenericMeta, type(typing.Union))):
        origin = target.__origin__
        args = target.__args__

        if target.__args__ is None:
            # like `typing.List`
            generic_type = target
            args = target.__parameters__
        else:
            # like `typing.List[int]`
            generic_type = origin
            args = target.__args__

        args = tuple(get_type_info(g) for g in args)

        if generic_type is typing.Union:
            return from_union(target, args)

        if generic_type is typing.Type:
            return from_type(target, args)

        dynamic_type = _GENERICALIAS_GENERIC_DYNAMIC_MAP.get(generic_type)

        if dynamic_type in STD_TYPES:
            std_type = dynamic_type
        else:
            std_type = None

        return GenericTypeInfo(
            target,
            generic_type=generic_type,
            generic_args=args,
            dynamic_type=dynamic_type,
            std_type=std_type
        )

    elif isinstance(target, typing.TypeVar):
        constraints = tuple(get_type_info(t) for t in target.__constraints__)
        return TypeVarTypeInfo(target,
            constraints=constraints,
            covariant=target.__covariant__,
            contravariant=target.__contravariant__,
        )

    elif isinstance(target, type(typing.ClassVar)):
        raise TypeError('ClassVar is not a type')

    else:
        return TypeInfo(target)

