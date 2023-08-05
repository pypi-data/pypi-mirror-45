#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""TODO"""


# This file is part of Linshare cli.
#
# LinShare cli is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# LinShare cli is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with LinShare cli.  If not, see <http://www.gnu.org/licenses/>.
#
# Copyright 2019 Frédéric MARTIN
#
# Contributors list :
#
#  Frédéric MARTIN frederic.martin.fma@gmail.com
#

from __future__ import unicode_literals

import datetime
import logging

from hurry.filesize import size as filesize
from hurry.filesize import si


def format_repr(obj, name, value):
    """TODO"""
    res = """
    - {0:9} : {1}
    - {2:9} : {3}
    - {4:9} : {5} {6}
    - {7:9} : {8}""".format(
        "class", type(obj),
        "property", name,
        "value", value, type(value),
        "str", obj
    )
    return res


class CellBuilder(object):
    """TODO"""
    # pylint: disable=too-few-public-methods

    def __init__(self, name, raw=False, vertical=False):
        self.clazz = None
        self.name = name
        self.raw = raw
        self.vertical = vertical
        classname = str(self.__class__.__name__.lower())
        self.log = logging.getLogger("linsharecli.common." + classname)

    def __call__(self, value):
        if self.clazz is None:
            if self.name in ["creationDate", "modificationDate", "expirationDate"]:
                self.clazz = DateCell
            elif self.name in ["size"]:
                self.clazz = SizeCell
            elif isinstance(value, int):
                self.clazz = ICell
            else:
                self.clazz = SCell
            # ["domain", "actor"]:
        self.log.debug("value: %s", value)
        self.log.debug("value type: %s", type(value))
        self.log.debug("name: %s", self.name)
        self.log.debug("raw: %s", self.raw)
        self.log.debug("vertical: %s", self.vertical)
        cell = self.clazz(value)
        cell.name = self.name
        cell.raw = self.raw
        cell.vertical = self.vertical
        self.log.debug(repr(cell))
        return cell


class SCell(str):
    """TODO"""
    # pylint: disable=too-few-public-methods

    def __init__(self, value):
        super(SCell, self).__init__(value)
        self.value = value
        self.raw = False
        self.vertical = False
        self.name = None

    def __repr__(self):
        return format_repr(self, self.name, self.value)

    def __str__(self):
        return str(self.value)


class DateCell(object):
    """TODO"""

    # pylint: disable=too-few-public-methods
    def __init__(self, value):
        self.value = value
        self.raw = False
        self.vertical = False
        self._d_formatt = "{da:%Y-%m-%d %H:%M:%S}"
        self.name = None

    def __repr__(self):
        return format_repr(self, self.name, self.value)

    def __str__(self):
        if self.raw:
            return str(self.value)
        if self.value is not None:
            # if self.vertical:
            #     self._d_formatt = "{da:%Y-%m-%d}"
            return self._d_formatt.format(
                da=datetime.datetime.fromtimestamp(self.value / 1000))
        return "-"

    # def __cmp__(self, value):
        # if self.value == value:



class ICell(int):
    """TODO"""
    # pylint: disable=too-few-public-methods

    def __init__(self, value):
        super(ICell, self).__init__(value)
        self.value = value
        self.raw = False
        self.vertical = False
        self.name = None

    def __repr__(self):
        return format_repr(self, self.name, self.value)

    def __str__(self):
        if self.raw:
            return str(self.value)
        return str(self.value)


class SizeCell(int):
    """TODO"""
    # pylint: disable=too-few-public-methods

    def __init__(self, value):
        super(SizeCell, self).__init__(value)
        self.value = value
        self.raw = False
        self.vertical = False
        self.name = None

    def __repr__(self):
        return format_repr(self, self.name, self.value)

    def __str__(self):
        if self.raw:
            return str(self.value)
        return filesize(self.value, system=si)


class Cell2(object):
    """TODO"""
    # pylint: disable=too-few-public-methods

    def __init__(self, value):
        self.value = value
        self.raw = value
        self.l_format = None

    def __repr__(self):
        res = []
        res.append(">---")
        res.append(super(Cell2, self).__repr__())
        res.append(str(self.raw))
        res.append(str(self))
        res.append("---<")
        return "\n - ".join(res)

    def __str__(self):
        # if isinstance(vals, dict):
        if self.l_format:
            return self.l_format.format(**self.raw)
        return str(self.value)

    def keys(self):
        """TODO"""
        return self.value.keys()

    def __getitem__(self, key):
        return self.value[key]

class ICell2(int):
    """TODO"""
    # pylint: disable=too-few-public-methods

    def __init__(self, value):
        super(ICell2, self).__init__(value)
        self.value = value
        self.raw = value

    def __str__(self):
        return str(self.value)

    # def __div__(self, value):
    #     return self.value / value


# class SizeFormatter(Formatter):
#     """TODO"""
# 
#     def __init__(self, prop, empty=None):
#         super(SizeFormatter, self).__init__(prop)
#         self.empty = empty
# 
#     def __call__(self, row, context=None):
#         lsize = row.get(self.prop)
#         print repr(lsize)
#         if lsize is not None:
#             row[self.prop].value = filesize(lsize, system=si)
#             print row[self.prop].value
#             lsize = row.get(self.prop)
#             print repr(lsize)
#         else:
#             if self.empty:
#                 row[self.prop] = self.empty
# 
# class GenericFormatter(Formatter):
#     """Convert resource domain value to a readable name"""
# 
#     def __init__(self, prop, full=False):
#         super(GenericFormatter, self).__init__(prop)
#         self.full = full
# 
#     def __call__(self, row, context=None):
#         parameter = row.get(self.prop)
#         # print ">--", parameter, type(parameter), "--<"
#         # print ">--", parameter, type(parameter), parameter.raw, "--<"
#         if parameter:
#             print repr(parameter)
#             l_format = '{name}'
#             if context.args.vertical:
#                 l_format = '{name} ({uuid})'
#             if self.full:
#                 l_format = '{name} ({uuid})'
#             l_format = '{name} | actor'
#             row[self.prop].l_format = l_format
#             row[self.prop].actor = row['actor'].raw['name']
# 
#             # row[self.prop].value = l_format.format(**parameter)
#             # row[self.prop].value += " | "
#             # row[self.prop].value += row['actor'].raw['name']
#             # for i in range(5):
#             #     row[self.prop].value += "\n"
#             print repr(parameter)
#             # print ">--", parameter, type(parameter), parameter.raw, "--<"
# 
