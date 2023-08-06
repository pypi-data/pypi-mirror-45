# -*- coding: utf-8 -*-
#
# Copyright (c) 2019~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import sys

assert sys.version_info.major == 3

if sys.version_info.minor > 6:
    from ._py37_impl import get_type_info

elif sys.version_info.minor == 6:
    from ._py36_impl import get_type_info
