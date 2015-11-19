#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# https://github.com/MrNasro/scripts/blob/master/exploits/rom0x/rom0x.sh
#


import os
from struct import unpack
from lib.lzs import Block, LZSDecompress

fname = 'rom-0asdasd'
# fname = 'rom-0'
with open(os.path.join('tmp', fname), 'rb') as fd:
    # get spt.dat
    # dd if=/tmp/rom-0 of=/tmp/spt.dat bs=1 skip=8552 count=39600
    # dd if=/tmp/spt.dat of=/tmp/data bs=1 count=220 skip=16
    fpos = 8568
    count = 220
    fd.seek(fpos)
    chunk = fd.read(count)

    data = LZSDecompress(chunk)[0]
    print data[20:].split('\x00')[0]
