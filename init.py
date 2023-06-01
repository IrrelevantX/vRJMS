#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import time
import subprocess

def makeqfile():
        p = subprocess.Popen(['python', 'generator.py', '250']) ## <-- nums of jobs
        time.sleep(15)
        return p
