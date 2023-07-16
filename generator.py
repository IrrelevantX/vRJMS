#!/usr/bin/env python3
#-*- coding: utf-8 -*-

from codecs import escape_encode
import os,sys,time
import random,math

def rewind(num):
    r = open('rewind','r')
    f = open('queue','a')
    for i in range(num):
        try:
            app, p, w, x, interval,pol1,pol2 = r.readline().split()
        except:
            try:
                app, p, w, x, interval,pol1 = r.readline().split()
                pol2 = ''
            except:
                app, p, w, x, interval = r.readline().split()
                pol1 = ''
                pol2 = ''
        f.write(app + ' ' + p  + ' ' + w + ' ' + x + pol1+ pol2 +'\n')
        f.flush()
        time.sleep(int(interval))

def generator(num):
    if os.path.exists("queue"):
        return
    apps = ['bt','cg','ep','ft','is','lu','mg','sp'] #ft is out due to problems with that specific job
    #apps = ['bt','cg','ep','is','lu','mg','sp']
    procs = [2**i for i in range(2,7)]
    classes = ['B']
    walltime = {
            'bt':[550, 230, 230, 80, 90, 80, 80, 80, 80],
            'cg':[120, 90, 70, 60, 90, 150, 120, 120, 120],
            'ep':[70, 40, 20, 10, 5, 3, 2, 2, 2],
            'ft':[100, 70, 60, 50, 60, 50, 80, 80, 80],
            'is':[10, 5, 5, 5, 10, 20, 10, 10, 10],
            'lu':[260, 170, 120, 60, 45, 50, 50, 50, 50],
            'mg':[20, 20, 10, 10, 10, 5, 5, 5, 5],
            'sp':[640, 470, 470, 160, 160, 130, 130, 130, 130]
            }

    r = open('rewind','a')
    f = open('queue','a')
    #########################
    #make the specific queue#
    #########################
    if 0:
        pproccs = [128,256,512]
        for c in ['D']:
            for i in pproccs:
                for j in apps:
                    #c = random.choice(classes)
                    w = walltime[j][int(math.log(i,2))-1]
                    f.write(j + '.' + c + '.' + 'x' + ' ' + str(i) + ' ' + str(w) + ' ' + str(0) + ' ' + str(1) + ' ' + str(random.randint(0,1)) +'\n')

        os.remove('rewind')
        return
    if 0: #<-- for specific queue
        for kkk in range(0,len(apps)):
            app_id = apps[kkk]
            app_comp = 'ft'
            c = random.choice(classes)
            pproccs = [8,16,32]
            for kk in pproccs:
                p = kk#random.choice(procs)
                p_fill = 64-2*p
                w_id = walltime[app_id][int(math.log(p,2))-1]
                w_comp = walltime[app_comp][int(math.log(64,2))-1]
                f.write(app_id + '.' + c + '.' + 'x' + ' ' + str(p) + ' ' + str(w_id) + ' ' + str(0) + ' ' + str(0) + ' ' + str(random.randint(0,1)) +'\n')
                for i in range(kkk,len(apps),2):
                    #p_fill_tmp = p_fill
                    f.write(app_comp + '.' + c + '.' + 'x' + ' ' + str(64) + ' ' + str(w_comp) + ' ' + str(0) + ' ' + str(1) + ' ' + str(random.randint(0,1)) +'\n')
                    # if p_fill_tmp >= 32:
                    #     w_fill = walltime[app_comp][int(math.log(32,2))-1]
                    #     p_fill_tmp -= 32
                    #     f.write(app_comp + '.' + c + '.' + 'x' + ' ' + str(32) + ' ' + str(w_fill) + ' ' + str(0) + ' ' + str(1) + ' ' + str(random.randint(0,1)) +'\n')
                    # if p_fill_tmp >= 16:
                    #     w_fill = walltime[app_comp][int(math.log(16,2))-1]
                    #     p_fill_tmp -= 16
                    #     f.write(app_comp + '.' + c + '.' + 'x' + ' ' + str(16) + ' ' + str(w_fill) + ' ' + str(0) + ' ' + str(1) + ' ' + str(random.randint(0,1)) +'\n')
                    # if p_fill_tmp >= 8:
                    #     w_fill = walltime['mg'][int(math.log(8,2))-1]
                    #     p_fill_tmp -= 8
                    #     f.write('mg' + '.' + c + '.' + 'x' + ' ' + str(8) + ' ' + str(w_fill) + ' ' + str(0) + ' ' + str(1) + ' ' + str(random.randint(0,1)) +'\n')
                    # if p_fill_tmp >= 4:
                    #     w_fill = walltime[app_comp][int(math.log(4,2))-1]
                    #     p_fill_tmp -= 4
                    #     f.write(app_comp + '.' + c + '.' + 'x' + ' ' + str(4) + ' ' + str(w_fill) + ' ' + str(0) + ' ' + str(1) + ' ' + str(random.randint(0,1)) +'\n')
                    f.write(app_id + '.' + c + '.' + 'x' + ' ' + str(p) + ' ' + str(w_id) + ' ' + str(0) + ' ' + str(0) + ' ' + str(random.randint(0,1)) +'\n')
                    app = apps[i]#random.choice(apps)
                    c = random.choice(classes)
                    #p = random.choice(procs)
                    w = walltime[app][int(math.log(p,2))-1]
                    f.write(app + '.' + c + '.' + 'x' + ' ' + str(p) + ' ' + str(w) + ' ' + str(0) + ' ' + str(0) + ' ' + str(random.randint(0,1)) +'\n')
                    if app == 'sp':
                        break
                    if kk == 32:
                        f.write(app_comp + '.' + c + '.' + 'x' + ' ' + str(64) + ' ' + str(w_comp) + ' ' + str(0) + ' ' + str(1) + ' ' + str(random.randint(0,1)) +'\n')
                    f.write(app_id + '.' + c + '.' + 'x' + ' ' + str(p) + ' ' + str(w_id) + ' ' + str(0) + ' ' + str(0) + ' ' + str(random.randint(0,1)) +'\n')
                    app = apps[i+1]#random.choice(apps)
                    c = random.choice(classes)
                    #p = random.choice(procs)
                    w = walltime[app][int(math.log(p,2))-1]
                    f.write(app + '.' + c + '.' + 'x' + ' ' + str(p) + ' ' + str(w) + ' ' + str(0) + ' ' + str(0) + ' ' + str(random.randint(0,1)) +'\n')
                f.write(app_comp + '.' + c + '.' + 'x' + ' ' + str(64) + ' ' + str(w_comp) + ' ' + str(0) + ' ' + str(1) + ' ' + str(random.randint(0,1)) +'\n')
        os.remove('rewind')
        return
    #############################
    #make the specific queue end#
    #############################
    for i in range(num):
        app = random.choice(apps)
        c = random.choice(classes)
        p =random.choice(procs) #<---- only 8 procs jobs 
        w = walltime[app][int(math.log(p,2))-1]
        interval = random.randint(3,10)
        endchar = '\n' #' ' if i%2==0 else '\n'
        r.write(app + '.' + c + '.' + 'x' + ' ' + str(p) + ' ' + str(w) + ' ' + str(0) + ' ' + str(interval) + ' ' +endchar)#'\n')
        f.write(app + '.' + c + '.' + 'x' + ' ' + str(p) + ' ' + str(w) + ' ' + str(0) + ' ' + str(random.randint(0,1)) + ' ' + str(random.randint(0,1)) +endchar)#'\n')
        f.flush()
        time.sleep(interval)
    r.close()
    f.close()
    os.remove('rewind')

if __name__ == '__main__':

    if os.path.exists('rewind'):
        rewind(int(sys.argv[1]))
    else:
        generator(int(sys.argv[1]))
