#!/usr/bin/env python

import argparse
import json
import pandas as pd
import requests

from bs4 import BeautifulSoup
from pprint import pprint


def get_value(v):
    if v is not None:
        if 'raw' in v:
            return v['raw']
        elif 'title' in v:
            return v['title']['raw']
    else:
        return v


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extract a GitHub project to CSV')
    parser.add_argument('--url', '-u', required=True, help="GitHub access token")
    #parser.add_argument('--token', '-t', required=True, help="GitHub access token")
    parser.add_argument('--output', '-o', required=True, help="Output filepath")
    args = parser.parse_args()

    # parse HTML
    html_text = requests.get(args.url).text
    soup = BeautifulSoup(html_text, 'html.parser')

    # extract script with column information
    columns_data = json.loads(soup.find(id='memex-columns-data').string)
    columns = {}
    for l in columns_data:
        columns[l['databaseId']] = l['name']

    # extract script with row content information
    items_data = json.loads(soup.find(id='memex-items-data').string)
    rows = []
    for l in items_data:
        t = {}
        for e in l['memexProjectColumnValues']:
            if e['memexProjectColumnId'] in columns:
                c = columns[e['memexProjectColumnId']]
                t[c] = get_value(e['value'])
            else:
                t[e['memexProjectColumnId']] = get_value(e['value'])
        rows.append(t)

    # transform rows dictionary to dataframe
    df = pd.DataFrame(rows)

    # export the dataframe to tsv output file
    df.to_csv(args.output, sep="\t", index=False)