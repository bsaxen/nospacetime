#============================================================
# File:   relation.py
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

if n == 4:
    inFile = sys.argv[1]
    from_node = int(sys.argv[2])
    to_node = int(sys.argv[3])
    tpl = inFile.split(".")
    outFile = 'S_'+tpl[0]+'_'+str(from_node)+'_'+str(to_node)+'.rel'
    outFileNt = 'S_'+tpl[0]+'_'+str(from_node)+'_'+str(to_node)+'.nt'
else:
    print ("Usage: python3 relation.py <nst-file> <from node> <to node> ")
    print ("OUTPUT: <out:relation_<from node>_<to node>.rel> ")
    exit()
#============================================================
def calcS3(S3): # Overall Signalling Information
#============================================================
    print ("===== calcS3 ======")
    global mx,dim

    wx = np.zeros((dim,dim))

    tx = mx.transpose()
    try:
        fh1 = open(outFile,'w')
    except:
        print ("Open file error1") 
    try:
        fh2 = open(outFileNt,'w')
    except:
        print ("Open file error2")     

    for node in range(0,dim):
        #print ("Seed Node="+str(node))
        seed = np.zeros(dim)
        seed[node] = 1
        #print(" ".join(map(str,seed.astype(int))))
        wx = np.copy(tx) 
        for step in range(0,dim-1): 
            #print ("********* step="+str(step))
            #print ("Step="+str(step))
            #print("\n".join(map(str,wx.astype(int))))
            work = np.einsum("ij,j->i", wx, seed)
            work = np.where(work > 0, 1, work)
            #print ("Work="+str(step))
            #print(" ".join(map(str,work.astype(int))))

            for ear in range(0,dim):
                S3[node][step][ear] = work[ear]
                if work[ear] != 0:
                    inode = node + 1
                    istep = step + 1
                    iear  = ear + 1
                    st = str(inode) + " " + str(istep) + " " + str(iear) + "\n"
                    fh1.write(st)
                    #print (st)
                    fh2.write("<http://nospacetime.com/node"+str(inode)+ ">\
                         <http://nospacetime.com/step"+str(istep)+">\
                         <http://nospacetime.com/node"+str(iear) + "> . \n")

            wx = np.einsum("ij, jk -> ik", wx, tx)
            wx = np.where(wx > 0, 1, wx)
    fh1.close()
    fh2.close()

    return
#============================================================
def triple(fh,seed, ear):
#============================================================
    #print ("===== triple ======")
    global dim,S3
    #print gfile
    #print "seed= " + str(gseed) + " ear= " + str(ear)
    spectrum = np.zeros(dim+1)

    unique = np.zeros((dim,dim))

    limit = 2**dim - 1

    if seed > limit or ear > limit:
        print("ERROR: s-node number too big " + str(ear) + " " + str(seed))
        return

    vx = np.zeros(dim)
    ex = np.zeros(dim)
    #signature = np.zeros(dim*2)
 
    b = "{0:b}".format(seed)
    e = "{0:b}".format(ear)
    #print ("dim="+str(dim))
    #print ("seed=" + b + "(" + str(seed) + ")")
    #print ("ear=" + e + "(" + str(ear) + ")")
    n = len(b)
    for i in range(0,n):
        #print "q " + str(i) + " " +b[i]
        vx[n-i-1] = b[i]
  
    n = len(e)
    for i in range(0,n):
        ex[n-i-1] = e[i]

    filename = "R3-"+str(seed)+"-"+str(ear)+".nt"
    filename_spectrum = str(seed)+'-'+str(ear)+'.spe'
    filename_r3 = str(seed)+'-'+str(ear)+'.r3'
    #slogan  = "/var/www/html/kunskapsgraf/R3-"+str(seed)+"-"+str(ear)

    try:
        fh_i = open(filename,'w')
    except:
        print ("Open R3 file error"+filename)    

    try:
        fh_sp = open(filename_spectrum,'w')
    except:
        print ("Open SPECTRUM file error"+filename_spectrum)    

    try:
        fh_r3 = open(filename_r3,'w')
    except:
        print ("Open r3 file error"+filename_r3)    

    sum1 = 0
    dim1 = 0
    for i in range(0,dim):
        if vx[i] == 1:
            for j in range(0,dim):
                if ex[j] == 1:
                    if i == j:
                        #fh_i.write("<http://x.com/"+str(i+1)+"-0"+ "> <http://x.com/relation"+"> <http://x.com/"+str(j+1)+"-0" + "> . \n")

                        #fh_i.write("<http://x.com/seed"+str(i+1)+ "> <http://x.com/relation> <http://x.com/step"+str(0) + "> . \n")
                        #fh_i.write("<http://x.com/step"+str(0)+ "> <http://x.com/relation> <http://x.com/ear"+str(j+1) + "> . \n")
                        #print ("seed=" + str(i+1) + " ear=" + str(j+1) + " step=0")
                        fh_i.write("<http://x.com/seed"+str(seed)+"_"+str(i+1)+ "> <http://x.com/step0> <http://x.com/ear"+str(ear)+"_"+str(j+1) + "> . \n")
                        #fh_r3.write( str(seed)+'_'+str(i+1)+ ' 0 '+str(ear)+'_'+str(j+1) + '\n')
                        dim1 = dim1 + 1
                        spectrum[0] += 1
                    for k in range(0,dim):
                        #print ("seed=" + str(i+1) + " ear=" + str(j+1) +" step=" + str(k))
                        #R3[i][k][j] = S3[i][k][j]
                        if S3[i][k][j] != 0:# and unique[i][j] == 0:
                            dim1 = dim1 + 1
                            unique[i][j] = 1
                            #print ("seed=" + str(i+1) + " ear=" + str(j+1) +" step=" + str(k+1))
                            #fh_i.write("<http://x.com/seed"+str(i+1)+ "> <http://x.com/relation> <http://x.com/step"+str(k+1) + "> . \n")
                            #fh_i.write("<http://x.com/step"+str(k+1)+ "> <http://x.com/relation> <http://x.com/ear"+str(j+1) + "> . \n")

                            fh_i.write("<http://x.com/seed"+str(seed)+"_"+str(i+1)+ "> <http://x.com/step"+str(k+1)+"> <http://x.com/ear"+str(ear)+"_"+str(j+1)+"> . \n")
                            if i != j: # Only external relations
                                fh_r3.write(str(seed)+'_'+str(i+1)+ ' ' + str(k+1) + ' ' +str(ear)+'_'+str(j+1) + '\n')
                            sum1 = sum1 + k + 1
                            spectrum[k+1] += 1
                            #fh_i.write("<http://x.com/"+str(i+1)+ "> <http://x.com/"+str(j+1)+"> <http://x.com/"+str(k+1) + "> . \n")
                            #fh_i.write("<http://x.com/"+str(i+1)+"-"+str(k+1)+ "> <http://x.com/relation"+"> <http://x.com/"+str(j+1)+"-"+str(k+1) + "> . \n")

    fh_i.close()

    for i in range(0,dim+1):
        itemp = int(spectrum[i])
        fh_sp.write(str(i)+" "+str(itemp)+"\n")

    fh_sp.close()
    fh_r3.close()


    if dim1 == 0:
        os.system("rm -f "+filename)
    #for i in range(1,dim):

    #slogan  = slogan + "-" + str(dim1) + "-" + str(sum1)
    slogan  = str(dim1) + "-" + str(sum1)
    #print ("Slogan="+slogan)
    if dim1 > 0:
        fh.write("<http://x.com/"+str(seed)+ "> <http://x.com/"+str(slogan)+"> <http://x.com/"+str(ear) + "> . \n") 

    return
#============================================================
def single(node1, node2):
#============================================================
    print ("===== single ======")
    global dim
    #maxNodeValue = 2**dim - 1
    filename = 'DESKTOP.nt'
    fh = open(filename,'w')
    #if node1 < maxNodeValue and node2 < maxNodeValue:
    triple(fh, node1, node2)
    triple(fh, node2, node1)
    fh.close()
    return
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
# fh_in = open(inFile,'r')

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





fh_in = open(inFile,'r')
count = 0
for line in fh_in:
    count += 1
    line = line.replace("\n","")
    if count == 1:
        dim = int(line)
        mx = np.zeros((dim,dim))
        print ('Dimension= '+str(dim))
    else:
        tpl = line.split(",")
        ssub = int(tpl[0])-1
        sobj = int(tpl[1])-1
        mx[ssub][sobj] = 1

fh_in.close()

striples = 2**dim -1
print( 'Objective Dimension: '+str(dim)+' '+'Triples: '+str(count)+' '+'Subjective Nodes: '+str(striples))

S3 = np.zeros((dim,dim,dim))
calcS3(S3)
single(from_node, to_node)

#============================================================
# End of File
#============================================================