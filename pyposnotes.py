#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2015 Michael Zapf <michael.zapf@fau.de>

"""

"""

import sys
from sys import argv
import argparse

sys.path.append('./python-escpos/build/lib.linux-x86_64-2.7/escpos')

from escpos import *

LINE_LENGTH = 42

def printBorderLine(p, border):
    p.text(border*(LINE_LENGTH/len(border)))
    p.control("LF")
#end def printBorderLine(p, border)

def printLineBordered(p, text, border):
    maxLen = LINE_LENGTH

    if len(border) > 0:
        maxLen -= 2
        maxLen -= 2*len(border)

    lines = [text[i:i+maxLen] for i in range(0, len(text), maxLen)]

    for line in lines:
        if len(border) > 0:
            p.text(border+" ")

        p.text(line)

        # padding
        if len(line) < maxLen:
            p.text(" "*(maxLen-len(line)))

        if len(border) > 0:
            p.text(" "+(border[::-1]))

        p.control("LF")
#end def printLineBordered(p, text, border)

def printStdin(p, border):
    data = sys.stdin.read()
    lines = data.splitlines()
    for line in lines:
        printLineBordered(Epson, line, border)
#end def printStdin(p)






# init argument parser
parser = argparse.ArgumentParser(description="Print some notes on an ESC/POS printer.")
parser.add_argument("--tty", nargs=1, default="/dev/ttyUSB0",
                    help="The serial tty device the printer is connected to.")
parser.add_argument("-i", "--interactive", action="store_const",
                    const=1, default=0,
                    help="Interactive mode. Asks for details interactively.")
args = parser.parse_args()
print "Called this program with arguments: "
print args


# init printer
Epson = printer.Serial(args.tty)
Epson.hw("INIT")

# print top border
printBorderLine(Epson, "*")
printLineBordered(Epson, " ", "*")

# interactive mode?
if args.interactive == 1:
    print "Title: "
    title = sys.stdin.readline()
    if len(title) > 1:
        print "Chosen title: " + title  # DEBUG
        #TODO: print title


# read whole data from stdin
printStdin(p, "*")

# draw end of border (bottom)
printLineBordered(Epson, " ", "*")
printBorderLine(Epson, "*")
Epson.cut()

