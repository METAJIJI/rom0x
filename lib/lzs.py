#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# https://gist.github.com/FiloSottile/4663892
# http://reverseengineering.stackexchange.com/questions/3662/backup-from-zynos-but-can-not-be-decompressed-with-lzs
#
##############################################################
# Lempel-Ziv-Stac decompression
# BitReader and RingList classes
#
#  Copyright (C) 2011  Filippo Valsorda - FiloSottile
# filosottile.wiki gmail.com - www.pytux.it
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see &lt;http://www.gnu.org/licenses/&gt;.
#
##############################################################

from collections import deque
from struct import unpack


class BitReader:
    """
    Gets a string or a iterable of chars (also mmap)
    representing bytes (ord) and permits to extract
    bits one by one like a stream
    """
    def __init__(self, b):
        self._bits = deque()

        for byte in b:
            byte = ord(byte)
            for n in xrange(8):
                self._bits.append(bool((byte >> (7-n)) & 1))

    def getBit(self):
        return self._bits.popleft()

    def getBits(self, num):
        res = 0
        for i in xrange(num):
            res += self.getBit() << num-1-i
        return res

    def getByte(self):
        return self.getBits(8)

    def __len__(self):
        return len(self._bits)

class RingList:
    """
    When the list is full, for every item appended
    the older is removed
    """
    def __init__(self, length):
        self.__data__ = deque()
        self.__full__ = False
        self.__max__ = length

    def append(self, x):
        if self.__full__:
            self.__data__.popleft()
        self.__data__.append(x)
        if self.size() == self.__max__:
            self.__full__ = True

    def get(self):
        return self.__data__

    def size(self):
        return len(self.__data__)

    def maxsize(self):
        return self.__max__

    def __getitem__(self, n):
        if n >= self.size():
            return None
        return self.__data__[n]

def LZSDecompress(data, window=RingList(2048)):
    """
    Gets a string or a iterable of chars (also mmap)
    representing bytes (ord) and an optional
    pre-populated dictionary; return the decompressed
    string and the final dictionary
    """
    reader = BitReader(data)
    result = ''

    while True:
        bit = reader.getBit()
        if not bit:
            char = reader.getByte()
            result += chr(char)
            window.append(char)
        else:
            bit = reader.getBit()
            if bit:
                offset = reader.getBits(7)
                if offset == 0:
                    # EOF
                    break
            else:
                offset = reader.getBits(11)

            lenField = reader.getBits(2)
            if lenField < 3:
                lenght = lenField + 2
            else:
                lenField <<= 2
                lenField += reader.getBits(2)
                if lenField < 15:
                    lenght = (lenField & 0x0f) + 5
                else:
                    lenCounter = 0
                    lenField = reader.getBits(4)
                    while lenField == 15:
                        lenField = reader.getBits(4)
                        lenCounter += 1
                    lenght = 15*lenCounter + 8 + lenField

            for i in xrange(lenght):
                char = window[-offset]
                result += chr(char)
                window.append(char)

    return result, window

#
# http://codepad.org/a6k1D0IT
#
# class Object:
#     def __init__(self, blockdata, data):
#         self.name = data[:14].strip('\x00')
#         self.uncompsize = unpack('>H', data[14:16])[0]
#         self.compsize = unpack('>H', data[16:18])[0]
#         self.offset = unpack('>H', data[18:20])[0]
#         self.data = blockdata[self.offset:self.offset+self.compsize]
#         # print [self.data]
#         if self.name == 'spt.dat':
#             data2 = self.data
#             self.data = ''
#             index = 12
#             while index < self.uncompsize:
#                 orgsize = unpack('>H', data2[index:index+2])[0]
#                 rawsize = unpack('>H', data2[index+2:index+4])[0]
#                 print orgsize, rawsize
#                 self.data = LZSDecompress(data2[index+4:index+4+rawsize])[0]
#                 index += rawsize
#                 print self.data
#             print 'Password:', self.data[500:].split('\x00')[0]
#
# class Block:
#     def __init__(self, data):
#         self.blocknumber = ord(data[0])
#         self.unk1 = ord(data[1])
#         self.objectcount = unpack('>H', data[2:4])[0]
#         self.blocklength = unpack('>H', data[4:6])[0]
#
#         print 'self.blocknumber: %s\n' \
#               'self.objectcount: %s\n' \
#               'self.blocklength: %s\n' % (self.blocknumber, self.objectcount, self.blocklength)
#         import sys; sys.exit(1)
#
#         self.objects = []
#         for i in range(0, self.objectcount):
#             self.objects.append(Object(data, data[6+20*i:]))
