#!/usr/bin/python
# -*- coding: utf-8 -*-
import multiprocessing as mp
import os
import sys
from time import sleep

env = os.environ.get


def _check(filename):
    swp_filename = os.path.join(
        os.path.dirname(filename),
        '.' + os.path.basename(filename) + '.swp'
    )
    sleep(1)
    while True:
        if os.path.exists(swp_filename):
            sleep(1)
        else:
            return True


def _read(filename):
    with open(filename) as f:
        sys.stdout.write(f.read().rstrip('\n'))


def expire(func, args=(), timeout=1, default=False):
    pool = mp.Pool(processes=1)
    result = pool.apply_async(func, args=args)
    try:
        val = result.get(timeout=timeout)
    except mp.TimeoutError:
        pool.terminate()
        return default
    else:
        pool.close()
        pool.join()
        return val


def run(filename, timeout):
    r = expire(_check, args=(filename,), timeout=timeout)
    if r:
        _read(filename)
        os.remove(filename)
    else:
        pass #todo add notify


if __name__ == '__main__':
    tmp_f = sys.argv[1]
    timeout = int(env("timeout"), 30)
    run(tmp_f, timeout)
