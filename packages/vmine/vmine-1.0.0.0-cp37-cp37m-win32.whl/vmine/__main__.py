#!/usr/bin/env python
#-*- coding: utf-8 -*-
import os
import sys
from .main import VMine

def cseffects():
    folder = os.path.dirname(sys.executable)
    if sys.argv[0][-3:] == ".py":
        folder = os.path.dirname(os.path.realpath(sys.argv[0]))
    
    if len(sys.argv) > 1:
        vmine = VMine()
        if len(sys.argv) > 2:
            vmine.cseffects.input(sys.argv[1]).output(sys.argv[2])
        else:
            v = vmine.cseffects.input(sys.argv[1]).output()

if __name__ == "__main__":
    cseffects()