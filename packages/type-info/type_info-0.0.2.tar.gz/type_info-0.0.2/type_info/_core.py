# -*- coding: utf-8 -*-
#
# Copyright (c) 2019~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import typing
import collections

class TypeInfo:
    def __init__(self, target_type):
        self.target_type = target_type

    def __hash__(self):
        return hash(TypeInfo) ^ hash(self.target_type)

    def __eq__(self, value):
        if self is value:
            return True

        if isinstance(value, TypeInfo):
            return self.target_type == value.target_type

        if isinstance(value, type):
            return self.target_type == value

        return super().__eq__(value)

    def __repr__(self):
        return f'{type(self).__name__}({self.target_type!r})'

    @property
    def is_generic(self):
        return False

    def is_generic_closed(self):
        return True

    @property
    def is_typevar(self):
        return False


class GenericTypeInfo(TypeInfo):
    def __init__(self, target_type, *,
                 generic_type, generic_args, dynamic_type, std_type):
        super().__init__(target_type)

        self.generic_type = generic_type
        self.generic_args = generic_args

        # dynamic_type can be abs, std_type cannot be abs
        # `GenericTypeInfo(List[str]).std_type` is `list`
        # but `GenericTypeInfo(Iterable[str]).std_type` is None
        self.dynamic_type = dynamic_type
        self.std_type = std_type

    @property
    def is_generic(self):
        return True

    def is_generic_closed(self):
        return all(arg.is_generic_closed() for arg in self.generic_args)

    def __hash__(self):
        return hash(self.get_attrs_as_tuple())

    def __eq__(self, value):
        if self is value:
            return True

        if isinstance(value, GenericTypeInfo):
            return self.get_attrs_as_tuple() == value.get_attrs_as_tuple()

        return NotImplemented

    def get_attrs_as_tuple(self):
        return (
            self.generic_type,
            self.generic_args
        )


class TypeVarTypeInfo(TypeInfo):
    def __init__(self, target_type, *,
                 constraints, covariant, contravariant):
        super().__init__(target_type)

        self.typevar_constraints = constraints
        self.typevar_covariant = covariant
        self.typevar_contravariant = contravariant

    def is_generic_closed(self):
        return False

    @property
    def is_typevar(self):
        return True

    def __hash__(self):
        return hash(self.get_attrs_as_tuple())

    def __eq__(self, value):
        if self is value:
            return True

        if isinstance(value, TypeVarTypeInfo):
            return self.get_attrs_as_tuple() == value.get_attrs_as_tuple()

        if isinstance(value, typing.TypeVar):
            return self.get_attrs_as_tuple() == (
                value.__constraints__,
                value.__covariant__,
                value.__contravariant__
            )

        return NotImplemented

    def get_attrs_as_tuple(self):
        return (
            self.typevar_constraints,
            self.typevar_covariant,
            self.typevar_contravariant
        )


STD_TYPES = {
    dict,
    frozenset,
    list,
    set,
    tuple,

    # collections
    collections.ChainMap,
    collections.Counter,
    collections.defaultdict,
    collections.deque,
    collections.OrderedDict
}

def from_any():
    ''' get type info for `typing.Any` '''
    return TypeVarTypeInfo(
        typing.Any,
        constraints=(),
        covariant=False,
        contravariant=False
    )

def from_type(target, args):
    ''' get type info for `typing.Type[]` '''
    # like: typing.Type[str]
    return TypeVarTypeInfo(target,
        constraints=args,
        covariant=True,
        contravariant=False,
    )

def from_union(target, args):
    ''' get type info for `typing.Union[]` '''
    # union should be a typevar
    # this canbe parameter or return value
    # so `covariant` and `contravariant` should be `False`
    return TypeVarTypeInfo(target,
        constraints=args,
        covariant=False,
        contravariant=False,
    )

