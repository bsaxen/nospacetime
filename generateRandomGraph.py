#============================================================
# File:   generateRandomGraph.py
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

if n == 3:
    triples = int(sys.argv[1])
    dimension = int(sys.argv[2])
    outFile = 'random_'+str(triples)+'_'+str(dimension)+'.nst'
else:
    print ("Usage: python3 generateRandomGraph.py  <number of triples> <dimension> ")
    print ("OUTPUT FILE: random_<triples>_<dimension>.nst ")
    exit()
#============================================================
def createRandomTriples(fh,triples,nodes):
#============================================================
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


    print ("Number of random generated triples " + str(count))
    subNodes = 2**nodes -1
    print ("Subjective Number of Nodes: "+str(subNodes))
    return
#============================================================
# MAIN
#============================================================

fh_out = open(outFile,'w')
createRandomTriples(fh_out,triples,dimension)
fh_out.close()
print ("Triple file created: "+outFile)


#============================================================
# End of File
#============================================================


