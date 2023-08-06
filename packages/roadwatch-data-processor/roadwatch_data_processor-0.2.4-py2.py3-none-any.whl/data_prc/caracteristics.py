#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: caracteristics
   :platform: Unix, Windows
   :synopsis: A list of modifiers for 'caracteristiques' files

.. moduleauthor:: Daniel SASU <daniel.sasu@mail.com>

"""

import pandas as pd
import numpy as np
import datetime
from .core import process_generic_file

def put_gps_lat(row):
    """
    Format latitude as a float.

    :param row: a data frame row
    :type row: pandas.Series
    :returns: processed value.

    """
    if(row['lat'] == 0 and row['long'] == 0):
        row['long'] = 0
    else:
        row['lat'] = row['lat'] / 100000.0

    return row['lat']


def put_gps_long(row):
    """
    Format longitude as a float.

    :param row: a data frame row
    :type row: pandas.Series
    :returns: processed value.

    """
    if(row['lat'] == 0 and row['long'] == 0):
        row['long'] = 0
    else:
        row['long'] = row['long'] / 100000.0

    return row['long']


def put_timestamp(row):
    """
    Converts the date to a timestamp.

    :param row: a data frame row
    :type row: pandas.Series
    :returns: processed value.

    """
    return _create_timestamp(2000 + row['an'], row['mois'], row['jour'], row['hrmn'] // 100, row['hrmn'] % 100)


def put_insee(row):
    """
    Formats zip city zip code.

    :param row: a data frame row
    :type row: pandas.Series
    :returns: processed value.

    """
    return str(row['dep'])[:-1] + str(row['com'])


def _create_timestamp(year, month, day, hour, min):
    """
    Converts integers to a timestmp.
    """
    if year is None or month is None or day is None or hour is None or min is None:
        return None
    else:
        entry = datetime.datetime(year, month, day, hour, min)

        return entry


# SETTINGS FOR CARACTERISTICS
C_DTYPE = {
    'Num_Acc': pd.Int64Dtype(), 'jour': pd.Int64Dtype(), 'mois': pd.Int64Dtype(),
    'an': pd.Int64Dtype(), 'hrmn': pd.Int64Dtype(), 'dep': str, 'atm': pd.Int64Dtype(),
    'col': pd.Int64Dtype(), 'com': str, 'int': pd.Int64Dtype()
}

COLS_FORMATTED = [
    'lum', 'agg', 'int', 'atm', 'col', 'adr',
    'comm', 'dep', 'gps', 'lat', 'long', 'date'
]

C_MODIFIERS = {
    'lat': put_gps_lat,
    'long': put_gps_long,
    'date': put_timestamp,
    'comm': put_insee
}

COLS_DROP = [
    'an', 'mois', 'jour', 'hrmn', 'com'
]

COL_RENAME = [
    {'Num_Acc': 'num_acc'}
]


def process(path, index='num_acc', encoding='latin-1', sep=',', dtype=C_DTYPE,
            col_rename=COL_RENAME, cols_formatted=COLS_FORMATTED, modifiers=C_MODIFIERS, drop_cols=COLS_DROP):
    """
    Process a caractristics file.

    :param path: csv file path
    :type path: str
    :param index: index column
    :type index: str
    :param encoding: file encoding
    :type encoding: string
    :param sep: column separator
    :type sep: str
    :param dtype: data types for columns, the same structure as for pandas
    :type dtype: dict
    :param col_rename: a list of dict of the form { <old name>: <new name> }
    :type col_rename: list
    :param cols_formatted: column order
    :type cols_formatted: list
    :param modifiers: a set of modifier functions
    :type modifiers: dict
    :param drop_cols: a list of columns to be dropped
    :type drop_cols: list
    :returns: a processed dataFrame
    :rtype: pandas.DataFrame
    """
    return process_generic_file(path, index, encoding, sep, dtype, col_rename,
                                cols_formatted, modifiers, drop_cols)
