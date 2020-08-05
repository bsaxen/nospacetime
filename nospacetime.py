#============================================================
# File:   nospacetime.py
# Author: Benny Saxen
# Date:   2020-08-03
#============================================================
import sys,os
import random
import math
import numpy
import numpy as np
import time

resources = []
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
    tpl = line.split(" ")
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
    tpl = line.split(" ")
    ssub = int(tpl[0])
    sobj = int(tpl[1])
    fh_out.write (str(ssub)+' '+str(sobj)+'\n')
    triple = "<http://nospacetime.com#"+str(ssub) + "> <http://nospacetime.com#relation"+ "> <http://nospacetime.com#" + str(sobj) + "> . \n"
    fh_nt.write (triple)

 
fh_in.close()

fh_out.close()
fh_nt.close()


