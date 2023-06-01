#!/usr/bin/env python3
#-*- coding: utf-8 -*-

class JobStats:
    def __init__(self,id,name,procs,confpol,actualpol):
        self.id = id
        self.name = name
        self.Class = name[3]
        self.procs= procs
        self.ConfPolicy = confpol
        self.ActualPolicy = actualpol
        self.RunOn = ''
        self.RunWith = ''
        self.time = ''
    def __str__(self):
        return str(self.id) + " " + self.name + ' ' +str(self.procs) + ' ' +self.ConfPolicy + ' ' +self.ActualPolicy + ' ' +self.RunOn + ' ' +self.RunWith + ' ' + self.time