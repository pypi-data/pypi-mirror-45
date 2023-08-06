#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: departement
   :platform: Unix, Windows
   :synopsis: A list of modifiers for 'geojson files'

.. moduleauthor:: Daniel SASU <daniel.sasu@mail.com>

"""

import json
import pandas as pd

def _get_empty_dep_frame():
    """
    Creates an empty departement entry

    :returns: an empty departement entry.
    :rtype: dict

    """
    return {
    'id': [],
    'nom': [],
    'geometry':[],
}

def _format_code(code):
    """
    Format departement code (Add a 0 at the end if the length < 0).

    :returns: formatted code
    :rtype: str


    """
    if len(code) < 3:
        return code + '0'
    return code


def process(path):
    """
    Creates a data frame from geojson file

    :param path: a geojson file
    :type path: str
    :returns: a dataframe
    :rtype: pandas.DataFrame
    """
    with open(path, 'r') as json_file:
        data = json.load(json_file, parse_int=str)
        deps = _get_empty_dep_frame()
        # print(data['features'][0]['properties'].keys())
        # print(data['features'][0]['geometry'].keys())
        for dep in data['features']:
            deps['id'].append(_format_code(dep['properties']['code']))
            deps['nom'].append(dep['properties']['nom'])
            deps['geometry'].append(json.dumps(dep['geometry']))


        df = pd.DataFrame(data=deps)
        df.set_index('id', inplace=True)
        return df
