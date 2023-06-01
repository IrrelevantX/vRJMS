#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import argparse,time
import yaml
import math
import aux_py as aux
import shared,stats

from matplot import Plot
from manager import Manager

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description = 'A parser used to obtain information concerning the resource manager. Also used to display state of execution.', usage = './main.py [-h] [-c C] [-l L] [-v]', add_help = False)
    parser.add_argument('-h', '--help', action='help', default = argparse.SUPPRESS, help = 'Show this help message and exit.')
    parser.add_argument('-c', '-config', metavar = ('FILEPATH'), nargs = '?', required = False, default = 'config/compact.yaml', type = str, help = 'The yaml file with the configuration for the job scheduler.')
    parser.add_argument('-i', '-info', required = False, help = 'Show information about the cluster. Accepted values: queue, state.')
    args = parser.parse_args()

    if args.i:
        with open(args.c) as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
            with open(config['State']) as f:
                tokens = f.readlines()
                i = tokens.index('\n')
                if args.i == 'queue':
                    lines = tokens[:i]
                    lines.sort(key = lambda line: int(line.split()[0]))
                    headers = ['Id', 'App', 'Procs', 'Status', 'Started', 'Remaining']
                    text = aux.format(headers)
                    for line in lines:
                        line = line.split(' ' + ' ')
                        if line[3] == 'R':
                            date, time = line[-2].split()
                            runtime = aux.elapsed(aux.todatetime(date, time))
                            line[-1] = aux.timew(int(line[-1]) - runtime)
                            line[-2] = time
                        else:
                            line[-1] = aux.timew(int(line[-1]))
                            line[-2] = '-'
                        text += aux.format(line)
                    aux.prettyprint(text)
                elif args.i == 'state':
                    lines = tokens[i+1:]
                    headers = ['Node', 'Socket', 'Taken', 'Status'] + ['Core' + ' ' + str(num) for num in range(config['Cores'])]
                    text = aux.format(headers)
                    for line in lines:
                        text += aux.format(line.split())
                    aux.prettyprint(text)
                else:
                    print('Provided invalid argument. See help for more info.')
    else:
        shared.init()
        with open(args.c) as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
            try:
                package = config['Selection']['LambdaLocation']
                name = config['Selection']['LambdaName']
                func = getattr(__import__(package, fromlist=[name]), name)
                if func == 'None':
                    func = None
            except:
                func = None
            try:
                Vars = config['Selection']['Variables'].replace(' ','').split(',')
            except:
                Vars = []
            try:
                alreadyrun = True if config['AlreadyRun'] else False
            except:
                alreadyrun = False
            heatmap = config['Applications']['Heatmap']
            manager = Manager(config['Nodes'], config['Sockets'], config['Cores'], config['Applications']['Path'], config['Applications']['Queue'], config['Log'], config['State'],func,Vars,alreadyrun, heatmap)
            algorithms = {'FCFS': lambda j: aux.elapsed(j.enter), 'WFP3': lambda j: math.pow(aux.elapsed(j.enter)/j.duration,3)*j.procs}
            if 1 or config['Allocation']['Policy'] == 'strip' or config['Allocation']['Policy'] == 'mixed': ##
                manager.readmap()
            TimeElapsed = time.time()
            job_stat = manager.scheduler(config['Allocation']['Policy'], algorithms[config['Scheduling']['Algorithm']], config['Scheduling']['Backfilling'])
            TimeElapsed = time.time() - TimeElapsed
            print(job_stat)
            print('{}({}):'.format(config['Scheduling']['Algorithm'],config['Scheduling']['Backfilling']), end = ' ')
            try:
                print(stats.avgs(config['Log'], shared.jobs))
            except:
                None
            print("Time elapsed : {}".format(TimeElapsed))
            try:
                package = config['Export']['ExportModuleFolder']+'.'+config['Export']['Module'] + "_module"
                name = config['Export']['Module']
                export = getattr(__import__(package, fromlist=[name]), name)
                print(job_stat[0])
                export(job_stat,config['Log'])
                print(job_stat[0])
            except:
                pass
            x = Plot(job_stat,config['Log'])