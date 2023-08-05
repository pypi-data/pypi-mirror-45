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
'''
Phase *history* container. When you think of a phase value, think of that value at
a specific point in time.

ATTENTION:
The species (list of Specie) AND quantities (list of Quantity) data members
have ARBITRARY density values either at an arbitrary point in the history or at
no point in the history. This needs to be removed in the future to avoid confusion.

To obtain history values, associated to the phase, at a particular point in time,
use the GetValue() method to access the history data frame (pandas) via columns and
rows. The corresponding values in species and quantities are OVERRIDEN and NOT to
be used through the phase interface.

Author: Valmor F. de Almeida dealmeidav@ornl.gov; vfda
Sat Sep  5 01:26:53 EDT 2015
'''
#*********************************************************************************
import os
import sys
from copy import deepcopy
import numpy as npy
import pandas

from cortix.support.specie   import Specie
from cortix.support.quantity import Quantity
#*********************************************************************************

class Phase():

    def __init__(self,
                 time_stamp = None,
                 species    = None,
                 quantities = None
                 ):

        if time_stamp is None:
            time_stamp = 0.0
        assert isinstance(time_stamp, float)

        if species is not None:
            assert isinstance(species, list)
            for specie in species:
                assert isinstance(specie, Specie)

        if quantities is not None:
            assert isinstance(quantities, list)
            for quant in quantities: 
                assert isinstance(quant, Quantity)

# List of species and quantities objects; columns of data frame are named
# by objects
        # a new object held by a Phase() object
        self.__species = deepcopy(species)
        # a new object held by a Phase() object
        self.__quantities = deepcopy(quantities)

        names = list()

        if species is not None:
            for specie in self.__species:
                names.append(specie.name)
                specie.massCC = 0.0  # clear these values
                                     # todo: eliminate them from Specie in the future

        if quantities is not None:
            for quant in self.__quantities:
                names.append(quant.name)
                quant.value = 0.0    # clear these values 
                                     # todo: eliminate them from Quantity in the future

# Table data phase without data type assigned; this is left to the user
# Time stamps will always be float
        self.__phase = pandas.DataFrame( index=[float(time_stamp)], columns=names )
#        self.__phase.fillna( 0.0, inplace=True )  # dtype defaults to float

        return

# *******************************************************************************
# Setters and Getters methods
# -------------------------------------------------------------------------------
# These are passing arguments by value effectively. Because the python objects
# passed into/out of the function are immutable.

    def GetActors(self):
        return list(self.__phase.columns)  # return all names in order

    def GetTimeStamps(self):
        return list(self.__phase.index)  # return all time stamps
    timeStamps = property(GetTimeStamps, None, None, None)

    def GetSpecie(self, name):
        for specie in self.__species:
            if specie.name == name:
                time_stamp = self.__get_time_stamp( None ) # get latest time stamp
                assert name in self.__phase.columns, 'name %r not in %r'% \
                   (name,self.__phase.columns)
                specie.massCC = self.__phase.loc[time_stamp, name]
                return specie  # return specie syncronized with the phase
        return None

    def GetSpecies(self):
        for species in self.__species:
          tmp = self.GetSpecie(species.name) # handy way to synchronize the whole list
        return self.__species
    species = property(GetSpecies, None, None, None)

    def GetQuantities(self):
        for quant in self.__quantities:
          tmp = self.GetQuantity(quant.name) # handy way to synchronize the whole list
        return self.__quantities
    quantities = property(GetQuantities, None, None, None)

    def SetSpecieId(self, name, val):
        for specie in self.__species:
            if specie.name == name:
                specie.flag = val
                return

    def GetQuantity(self, name):
        for quant in self.__quantities:
            if quant.name == name:
                time_stamp = self.__get_time_stamp( None ) # get latest time stamp
                assert name in self.__phase.columns, 'name %r not in %r'% \
                   (name,self.__phase.columns)
                quant.value = self.__phase.loc[time_stamp, name]
                return quant  # return quantity syncronized with the phase
        return None

    def AddSpecie(self, new_specie):
        assert isinstance(new_specie, Specie)
        assert new_specie.name not in list(self.__phase.columns), \
               'new_specie: %r exists. Current names: %r' % \
               (new_specie, self.__phase.columns)
        speciesFormulae = [specie.formulaName for specie in self.__species]
        assert new_specie.formulaName not in speciesFormulae
        self.__species.append(new_specie)
        newName = new_specie.name
        col = pandas.DataFrame( index=list(self.__phase.index), columns=[newName] )
        tmp = self.__phase
        df = tmp.join(col, how='outer')
        self.__phase = df.fillna(0.0)   # for species have float as default

    def AddQuantity(self, newQuant):
        assert isinstance(newQuant, Quantity)
        assert newQuant.name not in list(self.__phase.columns), \
               'quantity: %r exists. Current names: %r' % \
               (newQuant, self.__phase.columns)
        quantFormalNames = [quant.formalName for quant in self.__quantities]
        assert newQuant.formalName not in quantFormalNames
        self.__quantities.append(newQuant)
        newName = newQuant.name

        # create a col with object data type; user must fill out column 
        col = pandas.DataFrame( index=list( self.__phase.index), columns=[newName],
                                dtype=object )
        tmp = self.__phase
        df  = tmp.join(col, how='outer')
#        self.__phase = df.fillna(newQuant.value)

    def AddRow(self, try_time_stamp, row_values):
        assert isinstance(row_values, list)

        time_stamp = self.__get_time_stamp( try_time_stamp )
        assert time_stamp is None, 'already used time_stamp: %r'%(try_time_stamp)
        time_stamp = try_time_stamp

        assert len(row_values) == self.__phase.columns.size

        # create a row with object data type; users row_values data define data type
        row = pandas.DataFrame( index=[time_stamp], 
                                columns=list( self.__phase.columns ), dtype=object )

        for (col,v) in zip(row.columns, row_values):
            row.loc[time_stamp,col] = v

        frames = [self.__phase, row]
        self.__phase = pandas.concat(frames)
        return

    def GetRow(self, try_time_stamp=None):
        time_stamp = self.__get_time_stamp( try_time_stamp )
        assert time_stamp is not None, 'missing try_time_stamp: %r'%(try_time_stamp)
        return list(self.__phase.loc[time_stamp, :])

    def GetColumn(self, actor):
        assert isinstance(actor, str)
        assert actor in self.__phase.columns, 'actor %r not in %r'% \
                   (actor,self.__phase.columns)
        return list(self.__phase.loc[:, actor])

    def ScaleRow(self, try_time_stamp, value):
        assert isinstance(try_time_stamp, int) or isinstance(try_time_stamp, float) 
        time_stamp = self.__get_time_stamp( try_time_stamp )
        assert time_stamp is not None, 'missing try_time_stamp: %r'%(try_time_stamp)
        assert isinstance(value, int) or isinstance(value, float) 
        self.__phase.loc[time_stamp, :] *= value
        return

    # set species and quantities of history to a given value (default to zero value)
    # all time stamps are preserved
    def ClearHistory(self, value=0.0):
        assert isinstance(value, int) or isinstance(value, float) 
        self.__phase.loc[:, :] = value
        return

    # set species and quantities of history to a given value (default to zero value)
    # only one time stamp is preserved (default to last time stamp)
    def ResetHistory(self, try_time_stamp=None, value=None):
        if value is not None:
           assert isinstance(value, int) or isinstance(value, float) or \
                  isinstance(value, npy.ndarray)

        if try_time_stamp is not None:
           assert isinstance(try_time_stamp, int) or isinstance(try_time_stamp, float) 

        time_stamp = self.__get_time_stamp( try_time_stamp )
        assert time_stamp is not None, 'missing try_time_stamp: %r'%(try_time_stamp)

        values = self.GetRow(time_stamp)  # save values

        columns = list(self.__phase.columns)
        assert len(columns) == len(values), 'FATAL: oops internal error.'

        self.__phase = pandas.DataFrame( index=[time_stamp], columns=columns )
        self.__phase.fillna( 0.0, inplace=True )

        if value is None:
            for v in values:
                idx = values.index(v)
                self.__phase.loc[time_stamp, columns[idx]] = v  # restore values
        else:
            self.__phase.loc[time_stamp, :] = value   # set user-given value

        return

    def GetValue(self, actor, try_time_stamp=None):

        assert isinstance(actor, str)
        assert actor in self.__phase.columns, 'actor %r not in %r'% \
                   (actor,self.__phase.columns)

        if try_time_stamp is not None:
           assert isinstance(try_time_stamp, int) or isinstance(try_time_stamp, float) 

        time_stamp = self.__get_time_stamp( try_time_stamp )
        assert time_stamp is not None, 'missing try_time_stamp: %r'%(try_time_stamp)

        return self.__phase.loc[time_stamp, actor]

# old def SetValue(self, time_stamp, actor, value):
# new
    def SetValue(self, actor, value, try_time_stamp=None):

        assert isinstance(actor, str)
        assert actor in self.__phase.columns

#        assert isinstance(value, int) or isinstance(value, float) or \
#               isinstance(value, npy.ndarray)

        if try_time_stamp is not None:
           assert isinstance(try_time_stamp, int) or isinstance(try_time_stamp, float) 

        time_stamp = self.__get_time_stamp( try_time_stamp )
        assert time_stamp is not None, 'missing try_time_stamp: %r'%(try_time_stamp)

#        print('*value =', value)
#        print('*type(value) =', type(value))
#        print('*time_stamp =', time_stamp)
#        print('*actor =', actor)
#        print('*column values =', self.__phase[actor])
#        print('*df =', self.__phase)
#        print('*df.dtypes =', self.__phase.dtypes)
#        print('*df.shape =', self.__phase.shape)
#        print('')
#        if isinstance(value,npy.ndarray):
#           self.__phase[actor] = self.__phase.astype({actor:type(value)})
#        print('*df.dtypes =', self.__phase.dtypes)
#        print('')
        self.__phase.loc[time_stamp, actor] = value
        return

    def WriteHTML(self, fileName):
        assert isinstance(fileName, str)
        tmp = pandas.DataFrame(self.__phase)
        columnNames = tmp.columns
        speciesNames = [specie.name for specie in self.__species]
        quantityNames = [quantity.name for quantity in self.__quantities]
        for col in columnNames:
            if col in speciesNames:
                idx = speciesNames.index(col)
                specie = self.__species[idx]
                tmp.rename(columns={col: specie.formulaName}, inplace=True)
            elif col in quantityNames:
                idx = quantityNames.index(col)
                quant = self.__quantities[idx]
                tmp.rename( columns={ col: col + '[' + quant.unit + ']'},
                            inplace=True )
            else:
                assert False, 'oops fatal.'
        tmp.to_html(fileName)

#*********************************************************************************
# Private helper functions (internal use: __)

    def __get_time_stamp(self, try_time_stamp):
        """
        Helper method for finding the closest time stamp in the phase history.  
        The pandas Index container used for storing float data type time stamps
        will return the nearest time stamp up to a tolerance.
        """

        if try_time_stamp is None:
           return self.__phase.index[-1]
        else:
           tol = 1.0e-4
           try:
             loc = self.__phase.index.get_loc( try_time_stamp, method='nearest', 
                                               tolerance=tol )
           except KeyError:
             return None
           else:
             return  self.__phase.index[loc]

# *******************************************************************************
# Printing of data members
# def __str__( self ):
        s = '\n\t **Phase()**: \n\t *quantities*: %s\n\t *species*: %s\n\t *history* #time_stamp=%s\n\t *history end* @%s\n%s'
        return s % (self.__quantities, self.__species, len(self.__phase.index),
                    self.__phase.index[-1], self.__phase.loc[self.__phase.index[-1], :])
#

    def __repr__(self):
        s = '\n\t **Phase()**: \n\t *quantities*: %s\n\t *species*: %s\n\t *history* #time_stamp=%s\n\t *history end* @%s\n%s'
        return s % (self.__quantities, self.__species, len(self.__phase.index),
                    self.__phase.index[-1], self.__phase.loc[self.__phase.index[-1], :])
# *******************************************************************************
