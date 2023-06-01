#!/usr/bin/env python3
#-*- coding: utf-8 -*-

def NPB(jobs,logdir):
    for i in jobs:
        print('')
        with open(logdir +"/"+ i.name+'.'+str(i.id)+'.o','r') as f:
            print("***Job {} and id {} and procs {}".format(i.name,str(i.id),str(i.procs)))
            if i.ConfPolicy != '':
                print('    Configured Policy : {}, Actual policy : {}, Ran on hosts : {}'.format(i.ConfPolicy,i.ActualPolicy,i.RunOn))
            else:
                print('    Policy : {}, Ran on hosts : {}'.format(i.ActualPolicy,i.RunOn))
            if i.RunWith == '':
                print("    Ran alone")
            else:
                print("    Run with : {}".format(i.RunWith))
            out = f.readlines()
            if i.name.find('is') == -1:
                for k in out[::-1]:
                    if k.find('totcomm') != -1:
                        print("    Total comm : " +k.split()[-1],end = ' ' )
                        time = float(k.split()[-1])
                    elif k.find('totcomp') != -1:
                        print("Total com : " +k.split()[-1])
                        time += float(k.split()[-1])
                        print("    Total Time : " +str(time))
                        i.time = str(time)
                        break
            else:
                for k in out[::-1]:
                    if k.find('rcomm') != -1:
                        print("    Total comm : " +k.split()[-1],end = ' ' )
                        time = float(k.split()[-1])
                    elif k.find('rcomp') != -1:
                        print("Total com : " +k.split()[-1])
                        time += float(k.split()[-1])
                        print("    Total Time : " +str(time))
                        i.time = str(time)
                        break
