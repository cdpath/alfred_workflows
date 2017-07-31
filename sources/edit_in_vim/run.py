#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys

env = os.environ.get


def _read(filename):
    with open(filename) as f:
        sys.stdout.write(f.read().rstrip('\n'))
    os.remove(filename)


if __name__ == '__main__':
    tmp_f = env('filename')
    _read(tmp_f)
