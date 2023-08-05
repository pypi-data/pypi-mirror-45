#!/usr/bin/env python
#-*- coding: utf-8 -*-

from .plugins.cseffects.plugin import CSEffects

class VMine:
    def __init__(self):
        pass

    @property
    def cseffects(self):
        return CSEffects()
