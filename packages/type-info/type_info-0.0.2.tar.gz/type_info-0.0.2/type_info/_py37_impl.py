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

_GENERICALIAS_ORIGIN_GENERIC_MAP = {
    dict: typing.Dict,
    frozenset: typing.FrozenSet,
    list: typing.List,
    set: typing.Set,
    tuple: typing.Tuple,

    # collections
    collections.ChainMap: typing.ChainMap,
    collections.Counter: typing.Counter,
    collections.defaultdict: typing.DefaultDict,
    collections.deque: typing.Deque,

    # collections.abc
    collections.abc.AsyncGenerator: typing.AsyncGenerator,
    collections.abc.AsyncIterable: typing.AsyncIterable,
    collections.abc.AsyncIterator: typing.AsyncIterator,
    collections.abc.Awaitable: typing.Awaitable,
    collections.abc.ByteString: typing.ByteString,
    collections.abc.Collection: typing.Collection,
    collections.abc.Container: typing.Container,
    collections.abc.Coroutine: typing.Coroutine,
    collections.abc.Generator: typing.Generator,
    collections.abc.Hashable: typing.Hashable,
    collections.abc.ItemsView: typing.ItemsView,
    collections.abc.Iterable: typing.Iterable,
    collections.abc.Iterator: typing.Iterator,
    collections.abc.KeysView: typing.KeysView,
    collections.abc.Mapping: typing.Mapping,
    collections.abc.MappingView: typing.MappingView,
    collections.abc.MutableMapping: typing.MutableMapping,
    collections.abc.MutableSequence: typing.MutableSequence,
    collections.abc.MutableSet: typing.MutableSet,
    collections.abc.Reversible: typing.Reversible,
    collections.abc.Sequence: typing.Sequence,
    collections.abc.Set: typing.AbstractSet,
    collections.abc.Sized: typing.Sized,
    collections.abc.ValuesView: typing.ValuesView,
    collections.abc.Callable: typing.Callable,

    # contextlib
    contextlib.AbstractAsyncContextManager: typing.AsyncContextManager,
    contextlib.AbstractContextManager: typing.ContextManager,
}

if sys.version_info.micro > 1:
    _GENERICALIAS_ORIGIN_GENERIC_MAP.update({
        collections.OrderedDict: typing.OrderedDict,
    })

def get_type_info(target):
    if target is typing.Any:
        return from_any()

    if isinstance(target, typing._GenericAlias):
        origin = target.__origin__
        args = target.__args__
        args = tuple(get_type_info(g) for g in args)

        if origin is typing.Union:
            return from_union(target, args)

        elif origin is type:
            return from_type(target, args)

        elif origin is typing.ClassVar:
            raise TypeError('ClassVar is not a type')

        else:
            generic_type = _GENERICALIAS_ORIGIN_GENERIC_MAP.get(origin)

            if generic_type is not None:
                dynamic_type = origin
            else:
                dynamic_type = None

                if origin is typing.Generic:
                    generic_type = origin

                else:
                    raise NotImplementedError(origin)

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

    elif isinstance(target, typing._SpecialForm):
        raise NotImplementedError(target)

    else:
        return TypeInfo(target)

