#============================================================
# File:   nospacetime.py
# Author: Benny Saxen
# Date:   2020-08-07
#============================================================
import sys,os
import random
import math
import numpy
import numpy as np
import time

resources = []
#============================================================
def createRandomTriples(triples,nodes):
#============================================================
    n_triples = 0
    fh = open('nst.random','w')
    count = 0
    duplicate = 0
    mx = np.zeros((nodes+1,nodes+1))
    while count < triples:
        i = 0
    #for i in range(0,triples):

        ss = random.randint(1,nodes)
        oo = random.randint(1,nodes)

        while ss == oo:
            oo = random.randint(1,nodes)
            print (str(i) + " link to same node " + str(oo))

        duplicate = mx[ss][oo]
        while duplicate == 1:
            ss = random.randint(1,nodes)
            oo = random.randint(1,nodes)
            print (str(i) + " duplicate " + str(ss)+ ' '+ str(oo))
            duplicate = mx[ss][oo]
        
        if ss != oo and duplicate == 0:
            count += 1
            mx[ss][oo] = 1
            triple = str(ss) + "," +str(oo)
            fh.write(triple)
            fh.write('\n')
            print("triple "+str(ss)+','+str(oo))

        print("loop "+str(i))

    fh.close()
    print ("Number of random generated triples " + str(count))
#============================================================
def addResource(res):
#============================================================
    global resources

    nn = -1
    match = 0
    nr = len(resources)

    if nr == 0:
        resources.append(res)
        nn = 0
    else:
        i = 0
        while i < nr and match == 0: 
            if res == resources[i]:
                match = 1
                nn = i
            else:
                i += 1

        if match == 0:
            resources.append(res)
            nn = nr

    return nn
#============================================================
# Read graph 
#============================================================
dim = 0
fh_in = open("nst.in",'r')

n_triples = 0
for line in fh_in:
    n_triples += 1
    line = line.replace("\n","")
    tpl = line.split(",")
    ssub = int(tpl[0])
    sobj = int(tpl[1])

    sub = addResource(ssub) + 1
    obj = addResource(sobj) + 1

    if sub > dim:
        dim = sub
    if obj > dim:
        dim = obj
 
fh_in.close()

striples = 2**n_triples -1

print( 'Objective Dimension: '+str(dim)+' '+'Objective Triples: '+str(n_triples)+' '+'Subjective Triples: '+str(striples))

fh_out = open("nst.out",'w')
fh_nt = open("nst.nt",'w')
fh_out.write (str(dim)+'='+str(n_triples)+'\n')
fh_in = open("nst.in",'r')

for line in fh_in:
    line = line.replace("\n","")
    tpl = line.split(",")
    ssub = int(tpl[0])
    sobj = int(tpl[1])
    fh_out.write (str(ssub)+' '+str(sobj)+'\n')
    triple = "<http://nospacetime.com#"+str(ssub) + "> <http://nospacetime.com#relation"+ "> <http://nospacetime.com#" + str(sobj) + "> . \n"
    fh_nt.write (triple)

 
fh_in.close()

fh_out.close()
fh_nt.close()

createRandomTriples(100,100)


