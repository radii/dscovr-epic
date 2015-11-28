#!/usr/bin/env python

import sys
import json
import requests

r = requests.get('http://epic.gsfc.nasa.gov/api/images.php')
j = json.loads(r.text)

def exists(path):
    import os
    return os.access(path, os.F_OK)

png = bytearray()
for d in j:
    imgname = d['image']

    fname = "dscovr/%s.png" % imgname
    if exists(fname):
        print "already have %s" % fname
        continue

    url = "http://epic.gsfc.nasa.gov/epic-archive/png/%s.png" % imgname

    r = requests.get(url, stream=True)

    contentlength = int(r.headers['content-length'])
    png = bytearray()
    lastp = 0
    sys.stderr.write("%s len=%d\n" % (imgname, contentlength))
    for c in r.iter_content(chunk_size=1024):
        png.extend(c)
        p = int(len(png) * 100.0 / contentlength)
        if p != lastp:
            sys.stderr.write("\r%d/%d %d%%  " % (len(png), contentlength, p))
        lastp = p
    sys.stderr.write('\n')
    open(fname, "wb").write(png)

if j:
    open("dscovr/latest/latest.png", "wb").write(png)
