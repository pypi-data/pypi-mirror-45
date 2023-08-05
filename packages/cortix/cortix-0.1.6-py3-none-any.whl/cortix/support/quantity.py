#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of the Cortix toolkit environment
# https://cortix.org
#
# All rights reserved, see COPYRIGHT for full restrictions.
# https://github.com/dpploy/cortix/blob/master/COPYRIGHT.txt
#
# Licensed under the University of Massachusetts Lowell LICENSE:
# https://github.com/dpploy/cortix/blob/master/LICENSE.txt
"""
Author: Valmor de Almeida dealmeidav@ornl.gov; vfda

This Quantity class is to be used with other classes in plant-level process modules.

For unit testing do at the linux command prompt:
    python quantity.py

Sat Sep  5 12:51:34 EDT 2015
"""
# *******************************************************************************
import os
import sys
import numpy as npy
# *******************************************************************************

class Quantity():

    # todo: this probably should not have a "value" for the same reason as Specie.
    #      this needs some thinking.

    def __init__(self,
                 name='null-quantity',
                 formalName='null-quantity',
                 value=float(0.0),  # float, int, or npy.ndarray (float or int)
                 unit='null-unit'
                 ):

        assert isinstance(name, str), 'oops not string.'
        self._name = name

        assert isinstance(formalName, str), 'oops not string.'
        self._formalName = formalName

        assert isinstance(value, float) or isinstance(value, int) or  \
               isinstance(value, npy.ndarray),'illegal value.'

        if isinstance(value, npy.ndarray):
           assert value.dtype[:4] == 'float' or value.dtype[:2] == 'int'

        self._value = value

        assert isinstance(name, str), 'oops not string.'
        self._unit = unit

        self._name = name
        self._formalName = formalName
        self._value = value
        self._unit = unit

        return

# *******************************************************************************

# *******************************************************************************
# Setters and Getters methods
# -------------------------------------------------------------------------------
# These are passing arguments by value effectively. Because the python objects
# passed into/out of the function are immutable.

    def SetName(self, n):
        self._name = n

    def get_name(self):
        return self._name
    name = property(get_name, SetName, None, None)

    def SetValue(self, v):
        self._value = v

    def GetValue(self):
        return self._value
    value = property(GetValue, SetValue, None, None)

    def SetFormalName(self, fn):
        self._formalName = fn

    def GetFormalName(self):
        return self._formalName
    formalName = property(GetFormalName, SetFormalName, None, None)

    def SetUnit(self, f):
        self._unit = f

    def GetUnit(self):
        return self._unit
    unit = property(GetUnit, SetUnit, None, None)

# *******************************************************************************
# Internal helpers

# *******************************************************************************
# Printing of data members
    def __str__(self):
        s = '\n\t Quantity(): \n\t name=%s; formalName=%s; value=%s[%s]'
        return s % (self.name, self.formalName, self.value, self.unit)

    def __repr__(self):
        s = '\n\t Quantity(): \n\t name=%s; formalName=%s; value=%s[%s]'
        return s % (self.name, self.formalName, self.value, self.unit)


# *******************************************************************************
# Usage: -> python interface.py
if __name__ == "__main__":
    print('Unit testing for Quantity')
