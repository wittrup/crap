#!/usr/bin/env python
# -*- coding: utf-8 -*-


import json
import os.path


def is_non_zero_file(fpath):
    return os.path.isfile(fpath) and os.path.getsize(fpath) > 0

def jsloifex(filename, default={}):  # JSON load if exists
    return json.load(open(filename, encoding='utf-8')) if is_non_zero_file(filename) else default

def jsstfacp(obj, path, indent=None, separators=None, sort_keys=False, odpl=None):
    """ JSON store fix and create path
    :param obj:
    :param path:
    :param basename:
    :param indent:
    :param separators:
    :param sort_keys:
    :param odpl:
    :return: """
    head, tail = os.path.split(path)
    root, extension = os.path.splitext(tail)
    head += "/" if not (head.endswith("/") or head.endswith("\\")) else ""
    mkdir(head)
    extension += '.json' if not extension.endswith('.json') else ''
    path = os.path.join(head, root + extension)
    if odpl:  # One Dictionary Per Line
        with open(path, 'w', encoding="utf-8") as f:
            dump = json.dumps(obj, sort_keys=sort_keys)
            if type(obj) == list:
                f.write("[%s]" % ",\n ".join(map(json.dumps, obj)))
            elif type(obj) == dict:
                dump = dump.replace("}, ", "},\n")
                fili = dump[:dump.find("}")]  # First line
                sbac = fili.count("{")  # Start brackets count "{"
                sfux = [" " * findnthstr(fili, "{", i) for i in range(-1, sbac)]
                for line in dump.split("\n"):
                    stag = line.count("{")  # start tags/brackets
                    f.write(sfux[sbac - stag] + line + "\n")
            else:
                print('nothing to do here')
    else:
        json.dump(obj, open(path, 'w'), indent=indent, separators=separators, sort_keys=sort_keys)

def findnthstr(s, c, n):
    p = 0
    for i in range(n):
        p = s.find(c, p + 1)
    return p

def mkdir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)