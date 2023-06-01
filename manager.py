#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import os,subprocess
import math,datetime,time
import shared,init

from shutil import rmtree
from job import Job
from node import Node
from job_stats import JobStats

class Manager:
    def __init__(self, nodes, sockets, cores, appdir, queuefile, logdir, f,selectionFunc, Variables,alreadyrun, hmapfile = None):
        self.sockets = sockets
        self.cores = cores
        self.appdir = appdir
        self.queuefile = queuefile
        self.logdir = logdir
        self.hmapfile = hmapfile
        self.rankdir = os.path.join(os.getcwd(), 'rankfiles')
        self.piddir = os.path.join(os.getcwd(), 'pids')
        if os.path.exists(self.piddir):
            rmtree(self.piddir)
        if os.path.exists(self.rankdir):
            rmtree(self.rankdir)
        self.queue = []
        self.scheduled = set()
        self.heatmap = dict()
        self.f = f
        self.SelectionFunc = selectionFunc
        self.alreadyrun = alreadyrun
        self.nodes = []
        for num in range(nodes):
            self.nodes.append(Node('n' + str(num), sockets, cores))
        self.Vars = []
        for i in Variables:
            self.Vars.append(getattr(self,i))
        self.jobs = []

    #Read the heatmap
    def readmap(self):
        f = open(self.hmapfile, 'r')
        tokens = f.readline().split()
        while tokens:
            for num,token in enumerate(tokens):
                if not num:
                    key = token
                    self.heatmap[token] = dict()
                else:
                    self.heatmap[key][token] = num
            tokens = f.readline().split()

    #Read the queue starting from the line indicated by (index)
    def readqueue(self, index):
        f = open(self.queuefile, 'r')
        lines = f.readlines()[index:]
        id = index
        for line in lines:
            tokens = line.split()
            try:
                prefpolicy = 'compact' if self.SelectPolicy(self.Vars,tokens) else 'strip'
                self.queue.append(Job(id, tokens[0], int(tokens[1]), int(tokens[2]), datetime.datetime.now(), int(tokens[3]),prefpolicy))
                self.jobs.append(JobStats(id,tokens[0],tokens[1],'compact' if int(tokens[4]) else 'strip',prefpolicy))
                if len(tokens) > 10:
                    id += 1
                    if tokens[5].find('.') != -1:
                        offset = 5
                    else:
                        offset = 6
                    prefpolicy = 'compact' if self.SelectPolicy(self.Vars,tokens[offset:]) else 'strip'
                    tempjob = Job(id, tokens[offset + 0], int(tokens[offset + 1]), int(tokens[offset + 2]), datetime.datetime.now(), int(tokens[offset + 3]),prefpolicy)
                    if prefpolicy == 'strip':
                        self.queue[-1].CoSchedule = tempjob
                    elif prefpolicy == 'compact':
                        self.queue.append(tempjob)
                    self.jobs.append(JobStats(id,tokens[offset + 0],tokens[offset + 1],'compact' if int(tokens[offset + 4]) else 'strip',prefpolicy))
            except:
                self.queue.append(Job(id, tokens[0], int(tokens[1]), int(tokens[2]), datetime.datetime.now(), int(tokens[3]),''))
                self.jobs.append(JobStats(id,tokens[0],tokens[1],'','Preset'))
            id += 1
        return id

    def SelectPolicy(self, Vars, tokens):
        if self.SelectionFunc == None:
            return int(tokens[4])
        else:
            try:
                return int(self.SelectionFunc(Vars,tokens))
            except:
                return int(tokens[4])
    
    #Find backfilling time window 
    def backlog(self, job, nodes, i):
        occupied = [node for node in self.nodes if node not in nodes]
        window = map(lambda node: node.remaining(), occupied)
        job.runafter(sorted(window)[i-1])

    #Backfilling
    def backfill(self, policy):
        i = 1
        stripspace   = self.full('strip')
        compactspace = self.full('compact')
        if stripspace == 0 and compactspace == 0:
            return
        while i < len(self.queue):
            if self.queue[i].duration <= self.queue[0].interval:
                policy = self.queue[i].PrefPolicy if self.queue[i].PrefPolicy != '' else 'compact'
                if policy == 'compact' and compactspace == 0:
                    continue
                if policy == 'strip' and stripspace == 0:
                    continue
                if self.submit(self.queue[i], policy, 1):
                    job = self.queue.pop(i)
                    job.startedat(datetime.datetime.now())
                    self.scheduled.add(job)
                    shared.jobs.add(job)
                    if job.CoSchedule != None:
                        job.CoSchedule.startedat(datetime.datetime.now())
                        self.scheduled.add(job.CoSchedule)
                        shared.jobs.add(job.CoSchedule)
            i += 1

    #Find required nodes for a job
    def findnodes(self, job, policy, bf):
        if policy == 'compact':
            nodes = [node for node in self.nodes if not node.occupied(policy)]
            num = math.ceil(job.procs/(self.cores*self.sockets))
        elif policy == 'spare' or job.CoSchedule != None:
            nodes = [node for node in self.nodes if not node.occupied('spare')]
            num = math.ceil(2*job.procs/(self.cores*self.sockets))
        elif policy == 'strip':
            nodes = [node for node in self.nodes if not (node.occupied(policy) or node.exclusive) and (node.sockets[0].taken() + node.sockets[1].taken() <=(node.sockets[0].cores + node.sockets[1].cores)/2 )]
            nodes.sort(key = lambda node: node.precedence(self.heatmap, job))
            num = math.ceil(2*job.procs/(self.cores*self.sockets))
        if num > len(nodes):
            if bf and job == self.queue[0]:
                self.backlog(job, set(nodes), num-len(nodes))
            return []
        return nodes[:num]
    #Assign parallel tasks to processors
    def bind(self, nodes, job, pps):
        if not os.path.exists(self.rankdir):
            os.mkdir(self.rankdir)
        rem = job.procs
        rf = open(os.path.join(self.rankdir, job.app + '.' + str(job.id) + '.' + 'rf'), 'w')
        for num,node in enumerate(nodes):
            node.exclusive = job.exclusive
            for socket in node.sockets:
                while rem:
                    i = socket.freecore()
                    socket.jobs[i] = job
                    rf.write('rank' + ' ' + str(job.procs-rem) + '=+n' + str(num) + ' ' + 'slot=' + str(socket.num) + ':' + str(i) + '\n')
                    rem -= 1
                    if not rem%pps:
                        break
        return os.path.abspath(rf.name)

    #Run from shell
    def mpirun(self, hosts, job, rankfile):
        out = job.app + '.' + str(job.id) + '.' + 'o'
        err = job.app + '.' + str(job.id) + '.' + 'e'
        subprocess.call('echo '' > ' + self.piddir + '/' + str(job.id), shell = True)
        mpirun = 'mpirun -H ' + hosts + ' -np ' + str(job.procs) + ' -v --report-bindings --timestamp-output -rf ' + \
           rankfile + ' ' + self.appdir + '/' + job.app + ' 2>> ' + self.logdir + '/' + \
           err + ' 1>> ' + self.logdir + '/' + out + ' && '
        mpirun += 'rm' + ' ' + self.piddir + '/' + str(job.id) + '\n'
        subprocess.Popen(mpirun, shell = True)

    #Submit a job for execution
    def submit(self, job, policy, bf):
        if job.PrefPolicy == "strip":
            policy = 'spare' if job.exclusive else 'strip'
        elif job.PrefPolicy == "compact":
            policy = 'compact'
        elif policy == 'strip' and (job.exclusive or job.CoSchedule != None):
            policy = 'spare'
        nodes = self.findnodes(job, policy, bf)
        if nodes and policy == 'compact':
            rankfile = self.bind(nodes, job, self.cores)
        elif nodes and policy == 'spare':
            rankfile = self.bind(nodes, job, self.cores//2)
        elif nodes and policy == 'strip':
            isSpace = True
            for i in nodes:
                txt = str(i).splitlines()
                sock1 = txt[0].split()[2]
                sock2 = txt[1].split()[2]
                if int(sock1.split('/')[0])/int(sock1.split('/')[1]) > 0.5 or int(sock2.split('/')[0])/int(sock2.split('/')[1]) > 0.5:
                    isSpace = False
            if isSpace:
                rankfile = self.bind(nodes, job, self.cores//2)
            else:
                return 0
        else:
            return 0
        names = [node.name for node in nodes]
        hosts = '+' + ',+'.join(names)
        
        self.jobs[int(job.id)].RunOn = hosts
        if job.PrefPolicy == 'strip' or job.CoSchedule != None:
            for i in nodes:
                for k in str(i).splitlines():
                    if (job.app+'.'+str(job.id)) == k.split()[5] and k.split()[6] != '.' and self.jobs[int(job.id)].RunWith.find(k.split()[6]) == -1:
                        self.jobs[int(job.id)].RunWith += k.split()[6] + "|"
                        self.jobs[int(k.split()[6].split('.')[3])].RunWith += job.app+'.'+str(job.id) + '|'
                    elif (job.app+'.'+str(job.id)) == k.split()[6] and k.split()[5] != '.' and self.jobs[int(job.id)].RunWith.find(k.split()[5]) == -1:
                        self.jobs[int(job.id)].RunWith += k.split()[5] + "|"
                        self.jobs[int(k.split()[5].split('.')[3])].RunWith += job.app+'.'+str(job.id) + '|'
        self.mpirun(hosts, job, rankfile)
        if job.CoSchedule != None:
            rankfile = self.bind(nodes, job.CoSchedule, self.cores//2)
            self.jobs[int(job.CoSchedule.id)].RunOn = hosts
            for i in nodes:
                for k in str(i).splitlines():
                    if (job.CoSchedule.app+'.'+str(job.CoSchedule.id)) == k.split()[5] and k.split()[6] != '.' and self.jobs[int(job.CoSchedule.id)].RunWith.find(k.split()[6]) == -1:
                        self.jobs[int(job.CoSchedule.id)].RunWith += k.split()[6] + "|"
                        self.jobs[int(k.split()[6].split('.')[3])].RunWith += job.CoSchedule.app+'.'+str(job.CoSchedule.id) + '|'
                    elif (job.CoSchedule.app+'.'+str(job.CoSchedule.id)) == k.split()[6] and k.split()[5] != '.' and self.jobs[int(job.CoSchedule.id)].RunWith.find(k.split()[5]) == -1:
                        self.jobs[int(job.CoSchedule.id)].RunWith += k.split()[5] + "|"
                        self.jobs[int(k.split()[5].split('.')[3])].RunWith += job.CoSchedule.app+'.'+str(job.CoSchedule.id) + '|'
            self.mpirun(hosts, job.CoSchedule, rankfile)
        return 1
    
    #Job scheduler. Applies an algorithm by sorting the queue according to the (fun) parameter
    def scheduler(self, policy, fun, bf):
        flag = 0
        index = 0
        os.mkdir(self.piddir)
        p = init.makeqfile()
        start = time.time()
        varss = getattr(self,"nodes")
        while 1:
            end = time.time()
            self.free()
            index = self.readqueue(index)
            if self.alreadyrun:
                return self.jobs
            if self.queue:
                self.queue.sort(key = lambda job: (fun)(job), reverse = True)
                if self.submit(self.queue[0], policy, bf):
                    job = self.queue.pop(0)
                    job.startedat(datetime.datetime.now())
                    self.scheduled.add(job)
                    shared.jobs.add(job)
                    if job.CoSchedule != None:
                        job.CoSchedule.startedat(datetime.datetime.now())
                        self.scheduled.add(job.CoSchedule)
                        shared.jobs.add(job.CoSchedule)
                elif bf:#job or general pol
                    self.backfill(policy)
            elif self.empty() and p.poll()==0:
                os.rmdir(self.piddir)
                flag = 1
            self.snapshot()
            if flag:
                break
            time.sleep(5)
        return self.jobs

    #Free nodes from completed jobs
    def free(self):
        running = set(int(pid) for pid in os.listdir(self.piddir))
        for node in self.nodes:
            jobs = set(job for job in node.myjobs() if job.id not in running)
            if jobs:
                self.scheduled = self.scheduled.difference(jobs)
                node.free(jobs)

    #Check if the cluster is empty
    def empty(self):
        return not os.listdir(self.piddir)

    #Check if the cluster is full
    def full(self, policy):
        for node in self.nodes:
            if not node.occupied(policy):
                return 0
        return 1
    
    #Save the cluster's current state
    def snapshot(self):
        text = ''
        for job in set(self.queue).union(self.scheduled):
            text += str(job) + '\n'
        text += '\n'
        for node in self.nodes:
            text += str(node) +'\n'
        with open(self.f, 'w') as f:
            f.write(text[:-1])
