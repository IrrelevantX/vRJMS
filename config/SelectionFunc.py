#!/usr/bin/env python3
#-*- coding: utf-8 -*-

a = lambda Vars ,Job : Job[4] if Vars[0]*Vars[1]*len(Vars[2])/2 >= int(Job[1]) else 1
AllComp = lambda Vars,Jobs : 1
AllStrip = lambda Vars,Jobs : 0