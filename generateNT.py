#============================================================
# File:   generateNT.py
# Author: Benny Saxen
# Date:   2020-08-28
#============================================================
import sys,os
import random
import math
import numpy
import numpy as np
import time

resources = []
classUri = 'nospacetime.com#'
counter = 0
#============================================================
def createTriple(fh,sub, pre, obj, literal,s_uri,p_uri,o_uri,littype):
#============================================================
    global counter
    #print(sub+' '+pre+' '+obj)
    counter  += 1
    sub = sub.replace(" ","_")
    if pre == 'type':
        literal = 0 
    if literal == 0:
        obj = obj.replace(" ","_")
        if pre == "type":
            triple = '<http://'+s_uri+str(sub)+'> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type>  <http://'+o_uri+str(obj)+'> . \n'
        else:
            triple = '<http://'+s_uri+str(sub)+'> <http://'+p_uri+str(pre)+'>  <http://'+o_uri+str(obj)+'> . \n'

    if literal == 1:
        if len(obj) > 0:
            obj = obj.replace("\"","_")
            obj = obj.replace("\n","")
            if pre == "label":
                triple = '<http://'+s_uri+str(sub)+'> <http://www.w3.org/2000/01/rdf-schema#label>  \"'+str(obj)+'\" . \n'
            else:
                #print('++++++ '+sub+' '+pre+' '+obj+'---- '+s_uri+' '+p_uri+' '+o_uri)
                xtyp = '^^<http://www.w3.org/2001/XMLSchema#'+littype+'>'
                triple = '<http://'+s_uri+str(sub)+'> <http://'+p_uri+str(pre)+ '>  \"' +str(obj)+'\"'+xtyp+' . \n'
        else:
            #print("VOID"+str(len(obj)))
            triple = "void"

    if triple != 'void':
        fh.write(triple)

    return triple
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
def isKthBitSet(n, k): 
#============================================================
    if n & (1 << (k - 1)): 
        result = 1
    else: 
        result = 0
    return result 
#============================================================
# Read graph 
#============================================================
#dim = 0
fh_in = open(inFile,'r')

# n_triples = 0
# for line in fh_in:
#     n_triples += 1
#     line = line.replace("\n","")
#     tpl = line.split(",")
#     ssub = int(tpl[0])
#     sobj = int(tpl[1])

#     sub = addResource(ssub) + 1
#     obj = addResource(sobj) + 1

#     if sub > dim:
#         dim = sub
#     if obj > dim:
#         dim = obj
 
# fh_in.close()

# striples = 2**dim -1

# print( 'Objective Dimension: '+str(dim)+' '+'Triples: '+str(n_triples)+' '+'Subjective Nodes: '+str(striples))


fh_nt = open(ntFile,'w')
fh_in = open(inFile,'r')
count = 0
for line in fh_in:
    count += 1
    line = line.replace("\n","")
    if count == 1:
        dim = int(line)
        print ('Dimension= '+str(dim))
    else:
        tpl = line.split(",")
        ssub = int(tpl[0])
        sobj = int(tpl[1])
        node_sub = 'FOLKE_'+str(ssub)
        node_obj = 'FOLKE_'+str(sobj)
        createTriple(fh_nt,str(node_sub), 'type', 'folke', 0,classUri,classUri,classUri,'void')
        createTriple(fh_nt,str(node_obj), 'type', 'folke', 0,classUri,classUri,classUri,'void')
        createTriple(fh_nt,str(node_sub), 'link', str(node_obj), 0,classUri,classUri,classUri,'void')

fh_in.close()

nodes = 2**dim -1
for i in range(1,nodes):
    for j in range(1,dim+1):
        res = isKthBitSet(i, j)
        if res == 1:
            sub = 'NODE_'+str(i)
            obj = 'FOLKE_'+str(j)
            createTriple(fh_nt,str(sub), 'real', str(obj), 0,classUri,classUri,classUri,'void')
fh_nt.close()

print ("NT triple file created: "+ntFile)
#============================================================
# End of File
#============================================================