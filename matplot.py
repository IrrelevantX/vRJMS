#!/usr/bin/env python3
#-*- coding: utf-8 -*-
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

def Plot(jobs,logdir,SpeedUp):
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
        dix = {}
        # x4=[]
        # x8=[]
        # x16=[]
        # x32=[]
        # x64=[]
        name = kk
        jobs = sorted(jobs, key=lambda x:x.id ,reverse = False)
        for i in jobs:
            if i.name.find(name) != -1:
                # if int(i.procs) == 4:
                #     x4.append(float(i.time))
                # elif int(i.procs) == 8:
                #     x8.append(float(i.time))
                # elif int(i.procs) == 16:
                #     x16.append(float(i.time))
                # elif int(i.procs) == 32:
                #     x32.append(float(i.time))
                # elif int(i.procs) == 64:
                #     x64.append(float(i.time))
                if int(i.procs) not in list(dix.keys()):
                    dix[int(i.procs)] = []
                dix[int(i.procs)].append(float(i.time))
        # if x4 == [] and x8 ==[] and x16 == [] and x32 == [] and x64 == []:
        #     continue
        if len(list(dix.keys())) == 0:
            continue
        pltid += 1
        plt.figure(pltid)
        plt.title(name + " box plot times")
        #plt.boxplot([x4,x8,x16,x32],patch_artist=True,labels=['4','8','16','32'])
        plt.boxplot([dix[i] for i in list(dix.keys())],patch_artist=True,labels=list(dix.keys()))
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
            'sp' : []},
            'D' : {'bt' : [],
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
    for i in ['A','B','C','D']:
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
    
    # x = {
    #     'A' : {
    #             8 : {'bt' : [],
    #                 'cg' : [],
    #                 'ep' : [],
    #                 'ft' : [],
    #                 'is' : [],
    #                 'lu' : [],
    #                 'mg' : [],
    #                 'sp' : []},
    #             16: {'bt' : [],
    #                 'cg' : [],
    #                 'ep' : [],
    #                 'ft' : [],
    #                 'is' : [],
    #                 'lu' : [],
    #                 'mg' : [],
    #                 'sp' : []},
    #             32: {'bt' : [],
    #                 'cg' : [],
    #                 'ep' : [],
    #                 'ft' : [],
    #                 'is' : [],
    #                 'lu' : [],
    #                 'mg' : [],
    #                 'sp' : []}
    #                 },
    #     'B' : {
    #             8 : {'bt' : [],
    #                 'cg' : [],
    #                 'ep' : [],
    #                 'ft' : [],
    #                 'is' : [],
    #                 'lu' : [],
    #                 'mg' : [],
    #                 'sp' : []},
    #             16: {'bt' : [],
    #                 'cg' : [],
    #                 'ep' : [],
    #                 'ft' : [],
    #                 'is' : [],
    #                 'lu' : [],
    #                 'mg' : [],
    #                 'sp' : []},
    #             32: {'bt' : [],
    #                 'cg' : [],
    #                 'ep' : [],
    #                 'ft' : [],
    #                 'is' : [],
    #                 'lu' : [],
    #                 'mg' : [],
    #                 'sp' : []}
    #                 },
    #         'C' : {
    #             8 : {'bt' : [],
    #                 'cg' : [],
    #                 'ep' : [],
    #                 'ft' : [],
    #                 'is' : [],
    #                 'lu' : [],
    #                 'mg' : [],
    #                 'sp' : []},
    #             16: {'bt' : [],
    #                 'cg' : [],
    #                 'ep' : [],
    #                 'ft' : [],
    #                 'is' : [],
    #                 'lu' : [],
    #                 'mg' : [],
    #                 'sp' : []},
    #             32: {'bt' : [],
    #                 'cg' : [],
    #                 'ep' : [],
    #                 'ft' : [],
    #                 'is' : [],
    #                 'lu' : [],
    #                 'mg' : [],
    #                 'sp' : []}
    #                 },
    #         'D' : {
    #             8 : {'bt' : [],
    #                 'cg' : [],
    #                 'ep' : [],
    #                 'ft' : [],
    #                 'is' : [],
    #                 'lu' : [],
    #                 'mg' : [],
    #                 'sp' : []},
    #             16: {'bt' : [],
    #                 'cg' : [],
    #                 'ep' : [],
    #                 'ft' : [],
    #                 'is' : [],
    #                 'lu' : [],
    #                 'mg' : [],
    #                 'sp' : []},
    #             32: {'bt' : [],
    #                 'cg' : [],
    #                 'ep' : [],
    #                 'ft' : [],
    #                 'is' : [],
    #                 'lu' : [],
    #                 'mg' : [],
    #                 'sp' : []}
    #                 }
    # }
    General_X = []
    General_Y = []
    x = {}
    for i in list(SpeedUp.keys()):
        x[i] = {}
        for k in list(SpeedUp[i].keys()):
            x[i][k] = {}
            for j in list(SpeedUp[i][k].keys()):
                x[i][k][j] = {}
                x[i][k][j] = []
    for i in jobs:
        if (i.ActualPolicy == 'strip' or i.ActualPolicy == 'spare') and int(i.procs) in list(SpeedUp.keys()):
            x[int(i.procs)][i.name[3]][i.name[:2]].append(SpeedUp[int(i.procs)][i.name[3]][i.name[:2]]/float(i.time))
    for i in apps:
        labels = []
        xaxis = []
        for j in ['A','B','C','D']:
            for k in list(SpeedUp.keys()):
                try:
                    if x[k][j][i] != []:
                        xaxis.append(x[k][j][i])
                        labels.append(str(k)+"procs_"+j+"Class")
                except:
                    pass
        if xaxis != []:
            pltid += 1
            plt.figure(pltid)
            plt.title(i+'_Speed_up')
            plt.boxplot(xaxis,patch_artist=True,labels=labels)
            plt.savefig(logdir+'/{}.png'.format(i+'_Speed_up'))
            for count,elem in enumerate(xaxis):
                General_X.append(elem)
                General_Y.append(labels[count])
    # GENERAL SPEEDUP
    pltid += 1
    plt.figure(pltid)
    plt.title('General SpeedUp')
    plt.boxplot(General_X,patch_artist=True,labels=General_Y)
    plt.savefig(logdir+'/{}.png'.format('General_Speed_up'))
    return 1