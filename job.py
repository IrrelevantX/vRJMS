#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import aux_py as aux_py

class Job:
    def __init__(self, id, app, procs, duration, enter, exclusive,policy, start = None, interval = None):
        self.id = id
        self.app = app
        self.procs = procs
        self.duration = duration
        self.enter = enter
        self.exclusive = exclusive
        self.start = start
        self.interval = interval
        self.PrefPolicy = policy
        self.CoSchedule = None

    def startedat(self, timestamp):
        self.start = timestamp

    def runafter(self, interval):
        self.interval = interval

    def remaining(self):
        return round(self.duration-aux_py.elapsed(self.start))

    def state(self):
        return 'R' if self.start else 'Q'
    
    def ScoreFunciton(self):
        return

    def __str__(self):
        return str(self.id) + ' ' + ' ' +  self.app + ' ' + ' ' + str(self.procs) + ' ' + ' ' + self.state() + ' ' + ' ' + aux_py.tostring(self.start) + ' ' + ' ' + str(self.duration)
