#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: caracteristics
   :platform: Unix, Windows
   :synopsis: A list of modifiers for 'lieux files'

.. moduleauthor:: Daniel SASU <daniel.sasu@mail.com>

"""

import pandas as pd
import numpy as np
from rw_data_proc.core import process_generic_file

L_DTYPE = {
    'Num_Acc': int, 'catr': pd.Int64Dtype()
}

COLS_DROP = [
    'v1', 'v2', 'lartpc', 'larrout', 'env1'
]

L_MODIFIERS = {}

COLS_FORMATTED = []

COL_RENAME = [{'Num_Acc': 'num_acc'}]



def process(path, index='num_acc', encoding='latin-1', sep=',', dtype=L_DTYPE,
            col_rename=COL_RENAME, cols_formatted=COLS_FORMATTED, modifiers=L_MODIFIERS, drop_cols=COLS_DROP):
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
    ls = ['voie', 'circ', 'nbv', 'pr', 'pr1', 'plan', 'surf', 'infra', 'situ', 'vosp', 'prof']
    df = process_generic_file(path, index, encoding, sep, dtype, col_rename,
                                cols_formatted, modifiers, drop_cols)

    df[ls] = df[ls].fillna(0)
    df[ls] = df[ls].astype('int64')
    df[ls] = df[ls].astype('Int64')
    df[ls] = df[ls].replace(0, np.nan)

    return df
