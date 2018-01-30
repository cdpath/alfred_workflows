# -*- coding: utf-8 -*-

import sys

from parser import HTMLTableParser


def generate_markdown_table(table):
    table = iter(table[0])
    header = next(table)
    header = '|'.join(header)
    separator = '|'.join(['---']*len(header))
    sys.stdout.write(header+'\n')
    sys.stdout.write(separator+'\n')
    for t in table:
        t = '|'.join(t)
        sys.stdout.write(t+'\n')

query = sys.argv[1]

parser = HTMLTableParser()
parser.feed(query)

generate_markdown_table(parser.tables)
