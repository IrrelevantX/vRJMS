#!/usr/bin/env python3
#-*- coding: utf-8 -*-
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

def Plot(jobs,logdir):
    apps = {'bt' : 'green',
            'cg' : 'blue',
            'ep' : 'red',
            'ft' : 'black',
            'is' : 'brown',
            'lu' : 'pink',
            'mg' : 'purple',
            'sp' : 'orange'}
    jobs = sorted(jobs, key=lambda x:x.name ,reverse = False)
    prevname = ''
    ploting =[Line2D([0], [0], color='w',markerfacecolor='black',marker = 'o', label = 'compact',markersize=10),
              Line2D([0], [0], color='w',markerfacecolor='green',marker = 'v', label = 'strip',markersize=10),
              Line2D([0], [0], color='w',markerfacecolor='yellow',marker = 's', label = 'spare',markersize=10)]
    pltid = 1
    for i in jobs:
        if i.name == prevname:
            colour = "black" if i.ActualPolicy == 'compact' else apps[i.RunWith[:2]] if i.RunWith != '' else 'yellow'
            marker = "o" if i.ActualPolicy == 'compact' else 'v' if i.RunWith != '' else 's'
            plt.plot(int(i.procs), float(i.time), color=colour, marker=marker)
            continue
        if prevname != '':
            plt.legend(handles=ploting,bbox_to_anchor=(1, 0.5))
            plt.savefig(logdir+'/{}.png'.format(prevname))
            pltid += 1
            plt.figure(pltid)
        plt.title(i.name)
        plt.ylabel('Time')
        plt.xlabel('Procs')
        colour = "black" if i.ActualPolicy == 'compact' else apps[i.RunWith[:2]] if i.RunWith != '' else 'yellow'
        marker = "o" if i.ActualPolicy == 'compact' else 'v' if i.RunWith != '' else 's'
        plt.plot(int(i.procs), float(i.time), color=colour, marker=marker)
        prevname = i.name
    plt.legend(handles=ploting,bbox_to_anchor=(1, 0.5)      )
    plt.savefig(logdir+'/{}.png'.format(prevname))

#def ScatterPlot(jobs,logdir,pltid):
    pltid += 1
    plt.figure(pltid)
    x = []
    y = []
    colors = []
    area = []
    marker = []
    
    ploting = [Line2D([0], [0], color='w',markerfacecolor='black',marker = 'o', label = 'compact',markersize=15),
               Line2D([0], [0], color='w',markerfacecolor='black',marker = 'v', label = 'strip',markersize=15),
               Line2D([0], [0], color='w',markerfacecolor='green',marker = 'o', label = 'bt', markersize=15),
               Line2D([0], [0], color='w',markerfacecolor='blue',marker = 'o', label = 'cg', markersize=15),
               Line2D([0], [0], color='w',markerfacecolor='red',marker = 'o', label = 'ep', markersize=15),
               Line2D([0], [0], color='w',markerfacecolor='black',marker = 'o', label = 'ft', markersize=15),
               Line2D([0], [0], color='w',markerfacecolor='brown',marker = 'o', label = 'is', markersize=15),
               Line2D([0], [0], color='w',markerfacecolor='pink',marker = 'o', label = 'lu', markersize=15),
               Line2D([0], [0], color='w',markerfacecolor='purple',marker = 'o', label = 'mg', markersize=15),
               Line2D([0], [0], color='w',markerfacecolor='orange',marker = 'o', label = 'sp', markersize=15)]

    jobs = sorted(jobs, key=lambda x:x.procs ,reverse = True)

    maxtime = 0
    for i in jobs:
        x.append(int(i.procs))
        y.append(float(i.time))
        colors.append(apps[i.name[0:2]])
        area.append(100) if i.name.find('.A.') != -1 else area.append(200) if i.name.find('.B.') != -1 else area.append(300)
        marker.append("o") if i.ActualPolicy == 'compact' else marker.append('s') if i.RunWith == '' else marker.append('v')
        if float(i.time) > float(maxtime):
            maxtime = i.time
    N = len(jobs)
    for i in range(len(x)):
        plt.scatter(x[i],y[i],s=area[i],c=colors[i],marker=marker[i],alpha=0.5)
    plt.legend(handles=ploting,bbox_to_anchor=(0.95, 1.145),loc='upper right',ncol=5)
    plt.savefig(logdir+'/{}.png'.format("ScatterPlot"))
    
    
    #box plot
    apps = ['bt','cg','ep','ft','is','lu','mg','sp']
    for kk in apps:
        x4=[]
        x8=[]
        x16=[]
        x32=[]
        x64=[]
        name = kk
        jobs = sorted(jobs, key=lambda x:x.id ,reverse = False)
        for i in jobs:
            if i.name.find(name) != -1:
                if int(i.procs) == 4:
                    x4.append(float(i.time))
                elif int(i.procs) == 8:
                    x8.append(float(i.time))
                elif int(i.procs) == 16:
                    x16.append(float(i.time))
                elif int(i.procs) == 32:
                    x32.append(float(i.time))
                elif int(i.procs) == 64:
                    x64.append(float(i.time))
        if x4 == [] and x8 ==[] and x16 == [] and x32 == [] and x64 == []:
            continue
        pltid += 1
        plt.figure(pltid)
        plt.title(name + " box plot times")
        plt.boxplot([x4,x8,x16,x32],patch_artist=True,labels=['4','8','16','32'])
        plt.savefig(logdir+'/{}.png'.format(name + "_BoxPlot"))

    ### BOX FOR ALL ###
    pltid += 1 
    plt.figure(pltid)
    x = {
            'A' : {'bt' : [],
            'cg' : [],
            'ep' : [],
            'ft' : [],
            'is' : [],
            'lu' : [],
            'mg' : [],
            'sp' : []},
            'B' : {'bt' : [],
            'cg' : [],
            'ep' : [],
            'ft' : [],
            'is' : [],
            'lu' : [],
            'mg' : [],
            'sp' : []},
            'C' : {'bt' : [],
            'cg' : [],
            'ep' : [],
            'ft' : [],
            'is' : [],
            'lu' : [],
            'mg' : [],
            'sp' : []}
                }
    for i in jobs:
        x[i.name[3]][i.name[:2]].append(float(i.time))
    hor = []
    ver = []
    for i in ['A','B','C']:
        for j in apps:
            if x[i][j] != []:
                hor.append(x[i][j])
                ver.append(j+'.'+i)
    plt.title('General Box Plot times')
    plt.boxplot(hor,patch_artist=True,labels=ver)
    plt.savefig(logdir+'/{}.png'.format("General_BoxPlot"))
    
    ####################
    ## SPEED-UP CHART ##
    ####################
    SpeedUp = {
        8 : {
            'A' : {'bt' : 148.9558,
                'cg' : 29.7879,
                'ep' : 4.3377,
                'ft' : [],
                'is' : 12.9165,
                'lu' : 483.4307,
                'mg' : 11.1243,
                'sp' : 283.0192},
            'B' : {'bt' : 442.8837,
                'cg' : 433.0916,
                'ep' : 17.1335,
                'ft' : [],
                'is' : 55.6252,
                'lu' : 893.8568,
                'mg' : 55.4734,
                'sp' : 837.9894},
            'C' : {'bt' : 1391.601,
                'cg' : 747.6361,
                'ep' : 69.0313,
                'ft' : [],
                'is' : 216.2693,
                'lu' : 1445.9816,
                'mg' : 205.4686,
                'sp' : 2580.5323}
                },
        16: {
            'A' : {'bt' : 139.7494,
                'cg' : 40.6876,
                'ep' : 2.2193,
                'ft' : [],
                'is' : 6.5341,
                'lu' : 536.4487,
                'mg' : 11.5453,
                'sp' : 240.0954},
            'B' : {'bt' : 238.9611,
                'cg' : 432.5112,
                'ep' : 8.6856,
                'ft' : [],
                'is' : 21.918,
                'lu' : 907.4451,
                'mg' : 57.5277,
                'sp' : 471.0314},
            'C' : {'bt' : 692.4586,
                'cg' : 702.6995,
                'ep' : 34.153,
                'ft' : [],
                'is' : 64.6567,
                'lu' : 1159.1962,
                'mg' : 101.8392,
                'sp' : 1254.8695}
                },
        32: {
            'A' : {'bt' : 133.6288,
                'cg' : 44.7512,
                'ep' : 1.1824,
                'ft' : [],
                'is' : 5.9472,
                'lu' : 424.9609,
                'mg' : 8.5737,
                'sp' : 241.6503},
            'B' : {'bt' : 199.7763,
                'cg' : 364.96,
                'ep' : 4.419,
                'ft' : [],
                'is' : 12.34,
                'lu' : 638.2699,
                'mg' : 35.2513,
                'sp' : 361.1732},
            'C' : {'bt' : 377.165,
                'cg' : 595.3415,
                'ep' : 17.3709,
                'ft' : [],
                'is' : 41.7575,
                'lu' : 1101.4,
                'mg' : 88.7193,
                'sp' : 747.1371}
                }
    }
    x = {
        'A' : {
                8 : {'bt' : [],
                    'cg' : [],
                    'ep' : [],
                    'ft' : [],
                    'is' : [],
                    'lu' : [],
                    'mg' : [],
                    'sp' : []},
                16: {'bt' : [],
                    'cg' : [],
                    'ep' : [],
                    'ft' : [],
                    'is' : [],
                    'lu' : [],
                    'mg' : [],
                    'sp' : []},
                32: {'bt' : [],
                    'cg' : [],
                    'ep' : [],
                    'ft' : [],
                    'is' : [],
                    'lu' : [],
                    'mg' : [],
                    'sp' : []}
                    },
        'B' : {
                8 : {'bt' : [],
                    'cg' : [],
                    'ep' : [],
                    'ft' : [],
                    'is' : [],
                    'lu' : [],
                    'mg' : [],
                    'sp' : []},
                16: {'bt' : [],
                    'cg' : [],
                    'ep' : [],
                    'ft' : [],
                    'is' : [],
                    'lu' : [],
                    'mg' : [],
                    'sp' : []},
                32: {'bt' : [],
                    'cg' : [],
                    'ep' : [],
                    'ft' : [],
                    'is' : [],
                    'lu' : [],
                    'mg' : [],
                    'sp' : []}
                    },
            'C' : {
                8 : {'bt' : [],
                    'cg' : [],
                    'ep' : [],
                    'ft' : [],
                    'is' : [],
                    'lu' : [],
                    'mg' : [],
                    'sp' : []},
                16: {'bt' : [],
                    'cg' : [],
                    'ep' : [],
                    'ft' : [],
                    'is' : [],
                    'lu' : [],
                    'mg' : [],
                    'sp' : []},
                32: {'bt' : [],
                    'cg' : [],
                    'ep' : [],
                    'ft' : [],
                    'is' : [],
                    'lu' : [],
                    'mg' : [],
                    'sp' : []}
                    }
    }
    for i in jobs:
        if (i.ActualPolicy == 'strip' or i.ActualPolicy == 'spare') and int(i.procs) != 4:
            x[i.name[3]][int(i.procs)][i.name[:2]].append(float(i.time)/SpeedUp[int(i.procs)][i.name[3]][i.name[:2]])
    for i in apps:
        labels = []
        xaxis = []
        for j in ['A','B','C']:
            for k in [8,16,32]:
                if x[j][k][i] != []:
                    xaxis.append(x[j][k][i])
                    labels.append(str(k)+"procs_"+j+"Class")
        if xaxis != []:
            pltid += 1
            plt.figure(pltid)
            plt.title(i+'_Speed_up')
            plt.boxplot(xaxis,patch_artist=True,labels=labels)
            plt.savefig(logdir+'/{}.png'.format(i+'_Speed_up'))
    return 1