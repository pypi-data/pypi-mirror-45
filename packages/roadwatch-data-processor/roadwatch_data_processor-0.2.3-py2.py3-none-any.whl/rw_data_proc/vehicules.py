#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: vehicules
   :platform: Unix, Windows
   :synopsis: A list of modifiers for 'vehicules files'

.. moduleauthor:: Daniel SASU <daniel.sasu@mail.com>

"""

import pandas as pd
import numpy as np
from rw_data_proc.core import process_generic_file

V_DTYPE = {
    'Num_Acc': int, 'senc': pd.Int64Dtype(), 'catv':pd.Int64Dtype(),
    'obs': pd.Int64Dtype(), 'obsm': pd.Int64Dtype(), 'choc': pd.Int64Dtype(),
    'manv': pd.Int64Dtype(), 'occutc': pd.Int64Dtype()
}

COL_RENAME = [{'Num_Acc': 'accident_id'}]
COLS_FORMATTED = []
V_MODIFIERS = {}
COLS_DROP = []


def process(path, index=None, encoding='latin-1', sep=',', dtype=V_DTYPE,
            col_rename=COL_RENAME, cols_formatted=COLS_FORMATTED, modifiers=V_MODIFIERS, drop_cols=COLS_DROP):
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
    df = process_generic_file(path, index, encoding, sep, dtype, col_rename,
                                cols_formatted, modifiers, drop_cols)

    df.fillna(0, inplace=True)
    df.replace(0, np.nan, inplace=True)
    return df
