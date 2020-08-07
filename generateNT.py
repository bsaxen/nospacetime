#============================================================
# File:   generateNT.py
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
# Input
#============================================================
n = len(sys.argv)

if n == 2:
    inFile = sys.argv[1]
    tpl = inFile.split(".")
    ntFile = tpl[0]+'.nt'
else:
    print ("Usage: python3 generateNT.py <in:file.nst> ")
    print ("OUTPUT: <out:file.nt> ")
    exit()

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
fh_in = open(inFile,'r')

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

striples = 2**dim -1

print( 'Objective Dimension: '+str(dim)+' '+'Triples: '+str(n_triples)+' '+'Subjective Nodes: '+str(striples))


fh_nt = open(ntFile,'w')
fh_in = open(inFile,'r')

for line in fh_in:
    line = line.replace("\n","")
    tpl = line.split(",")
    ssub = int(tpl[0])
    sobj = int(tpl[1])
    triple = "<http://nospacetime.com#"+str(ssub) + "> <http://nospacetime.com#relation"+ "> <http://nospacetime.com#" + str(sobj) + "> . \n"
    fh_nt.write (triple)

fh_in.close()
fh_nt.close()

print ("NT triple file created: "+ntFile)
#============================================================
# End of File
#============================================================