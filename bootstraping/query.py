#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, '../')
import os
import argparse
import json
import logging
from datetime import datetime
from random import shuffle
from collections import defaultdict
from os.path import isfile
import grequests
from HelperModule.utils import file_to_list, query_string_or, jsonify_no


REQUEST_THREADS = 25


BASE_URL = 'http://localhost:9222/commoncrawl/sentence'
SEARCH_URL = BASE_URL + '/_search?size=250'

QUERY = ' {{"query" : {{"bool": {{"must": [{{"query_string": {{"default_field" : "text","query" : "(better OR worse OR superior OR inferior) AND {}"}}}}]}}}}}}'



def query(query_string, concept):
    """check if a, b property, qualifier and marker combination exists"""
    headers = {
        'Content-Type': 'application/json',
        'x-type': concept.replace('\\"', '')
    }

    return grequests.post(
        SEARCH_URL,
        data=query_string,
        headers=headers,
        timeout=60)



def main():

    requests = []
    requests.append(
        query(
            QUERY.format(jsonify_no(['cat', 'dog'], joiner=' AND ')),
            'cat-dog'))

    requests.append(
        query(
            QUERY.format(jsonify_no(['ruby', 'python'], joiner=' AND ')),
            'ruby-python'))

    requests.append(
        query(
            QUERY.format(jsonify_no(['OS X', 'Windows'], joiner=' AND ')),
            'osx-windows'))
    response = grequests.map(requests, size=REQUEST_THREADS, exception_handler=lambda x,y: print(y))
    for result in response:
        t = result.request.headers['x-type']
        with open('{}.json'.format(t), 'w') as out:
            json.dump( result.json(), out)




if __name__ == '__main__':
    main()
