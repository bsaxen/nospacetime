#============================================================
# File:   universe.py
# Author: Benny Saxen
# Date:   2020-12-26
#============================================================
import sys,os
import random
import math
import numpy
import numpy as np
import time

resources = []
mx_spec = []

classUri = 'nospacetime.com#'
counter = 0

hex2bin = dict('{:x} {:04b}'.format(x,x).split() for x in range(16))
bin2hex = dict('{:b} {:x}'.format(x,x).split() for x in range(16))
 
#============================================================
def float_dec2bin(d):
#============================================================  
    neg = False
    if d < 0:
        d = -d
        neg = True
    hx = float(d).hex()
    p = hx.index('p')
    bn = ''.join(hex2bin.get(char, char) for char in hx[2:p])
    res =  (('-' if neg else '') + bn.strip('0') + hx[p:p+2]
            + bin(int(hx[p+2:]))[2:])
    temp1 = bn.strip('0')
    temp2 = bin(int(hx[p+2:]))[2:]
    #print("1="+temp1)
    #print("2="+temp2)
    temp3 = int(temp2,2)
    #print(str(temp3))

    temp1 = temp1.replace(".","")
    
    left = temp1[0:temp3+1]
    right = temp1[temp3+1:len(temp1)]

    #print("left="+left)
    #print("right="+right)

    res = left+'.'+right
    return res
#============================================================
def float_bin2dec(bn):
#============================================================
    neg = False
    if bn[0] == '-':
        bn = bn[1:]
        neg = True
    dp = bn.index('.')
    extra0 = '0' * (4 - (dp % 4))
    bn2 = extra0 + bn
    dp = bn2.index('.')
    p = bn2.index('p')
    hx = ''.join(bin2hex.get(bn2[i:min(i+4, p)].lstrip('0'), bn2[i])
                 for i in range(0, dp+1, 4))
    bn3 = bn2[dp+1:p]
    extra0 = '0' * (4 - (len(bn3) % 4))
    bn4 = bn3 + extra0
    hx += ''.join(bin2hex.get(bn4[i:i+4].lstrip('0'))
                  for i in range(0, len(bn4), 4))
    hx = (('-' if neg else '') + '0x' + hx + bn2[p:p+2]
          + str(int('0b' + bn2[p+2:], 2)))
    return float.fromhex(hx)
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
def calcS3(S3): # Overall Signalling Information
#============================================================
    print ("===== calcS3 ======")
    global mx,dim

    wx = np.zeros((dim,dim))

    tx = mx.transpose()
    #try:
    #    fh1 = open(outFile,'w')
    #except:
    #   print ("Open file error1") 
    #try:
    #    fh2 = open(outFileNt,'w')
    #except:
    #    print ("Open file error2")     

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
                    #st = str(inode) + " " + str(istep) + " " + str(iear) + "\n"
                    #fh1.write(st)
                    #print (st)
                    #fh2.write("<http://s3.com/node"+str(inode)+ ">\
                    #     <http://s3.com/step"+str(istep)+">\
                    #     <http://s3.com/node"+str(iear) + "> . \n")

            wx = np.einsum("ij, jk -> ik", wx, tx)
            wx = np.where(wx > 0, 1, wx)
    #fh1.close()
    #fh2.close()

    return
#============================================================
def triple(fh_real,fh_global,fh_spectrum,seed, ear):
#============================================================
    #print ("===== triple ======")
    global dim,S3,caseName,mx_spec
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

    #rev_e = e[::-1]
    #rev_e = "{0:b}".format(rev_int_e)
    
    #real = b+'.'+rev_e + 'p+0'
    #print("Real="+real+" "+str(b)+"-"+str(e))
    #z = float_bin2dec(real)
    #print(z)
    #print ("dim="+str(dim))
    #print ("seed=" + b + "(" + str(seed) + ")")
    #print ("ear=" + e + "(" + str(ear) + ")")
    n = len(b)
    rb = 0
    for i in range(0,n):
        #print "q " + str(i) + " " +b[i]
        vx[n-i-1] = b[i]
        rb += int(b[i])*(2**(n-i-1))

  
    n = len(e)
    re = 0
    for i in range(0,n):
        ex[n-i-1] = e[i]
        re += int(e[i])*(0.5**(n-i))

    real = rb + re
    print('>'+str(real)+'   '+str(b)+'-'+str(e)+' seed:'+str(seed)+' ear:'+str(ear))
    print('>'+str(real)+'   '+str(rb)+'-'+str(re)+' seed:'+str(seed)+' ear:'+str(ear))
    filename = "R3-"+caseName+'_'+str(seed)+"-"+str(ear)+".nt"
    filename_spectrum = 'SPECTRUM_'+caseName+'_'+str(seed)+'-'+str(ear)+'.spe'
    filename_r3 = "R3-"+caseName+'_'+str(seed)+'-'+str(ear)+'.r3'


    sum1 = 0
    dim1 = 0
    for i in range(0,dim):
        if vx[i] == 1:
            for j in range(0,dim):
                if ex[j] == 1:
                    if i == j:
                        dim1 = dim1 + 1
                        spectrum[0] += 1
                    for k in range(0,dim):
                        if S3[i][k][j] != 0:# and unique[i][j] == 0:
                            dim1 = dim1 + 1
                            unique[i][j] = 1
                            sum1 = sum1 + k + 1
                            spectrum[k+1] += 1

    fh_spectrum.write(str(seed) + " " + str(ear)+":")
    fh_real.write(str(real))
    spec = ''
    zum = 0
    for i in range(0,dim):
        itemp = int(spectrum[i])
        zum += itemp*(i+1) 
        #fh_sp.write(str(i)+" "+str(itemp)+"\n")
        spec += str(itemp)+" "
        fh_spectrum.write(str(itemp)+" ")
    fh_real.write(' '+str(zum)+'\n')
    fh_spectrum.write("\n")
    szup = str(zum)
    mx_spec.append(spec)
    temp = spec.replace(" ","_")
    node_ear = 'NODE_'+str(ear)
    node_seed = 'NODE_'+str(seed)
    createTriple(fh_global,str(node_ear), 'type', 'Node', 0,classUri,classUri,classUri,'void')
    createTriple(fh_global,str(node_seed), 'type', 'Node', 0,classUri,classUri,classUri,'void')
    
    createTriple(fh_global,str(node_seed), 'out', temp, 0,classUri,classUri,classUri,'void')
    createTriple(fh_global,str(node_ear), 'in', temp, 0,classUri,classUri,classUri,'void')
    createTriple(fh_global,str(node_seed), temp,str(node_ear) , 0,classUri,classUri,classUri,'void')

    createTriple(fh_global,szup, 'type', 'Zum', 0,classUri,classUri,classUri,'void')
    createTriple(fh_global,temp, 'hasZum', szup, 0,classUri,classUri,classUri,'void')


    if dim1 == 0:
        os.system("rm -f "+filename)

    slogan  = str(dim1) + "-" + str(sum1)

    return
#============================================================
def single(fh_real,fh_g,fh_spectrum,node1, node2):
#============================================================
    global dim
    nones1 = bin(int(node1))[2:].count('1')
    nones2 = bin(int(node2))[2:].count('1')
    triple(fh_real,fh_g,fh_spectrum, node1, node2)

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
def sumList(inp):
#============================================================
    split = inp.split(" ")
    sum = 0
    for i in range(0,len(split)-1):
        sum += int(split[i])
    return(sum)
#============================================================
def family(tot,inp):
#============================================================
    fileName = 'work/FAM_'+str(tot)+'.fam'
    fh = open(fileName,"a+")
    fh.write(inp+'\n')
    fh.close()

#============================================================
# Main
#============================================================
n = len(sys.argv)

if n == 2:
    inFile = sys.argv[1]
    tpl = inFile.split(".")
    caseName = tpl[0]
else:
    print ("Usage: python3 relation.py <nst-file>  ")
    exit()


# Read graph 
dim = 0

os.system("rm -f work/*")
fh_real = open('real.txt','w')
fh_global = open('global.nt','w')

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

#======================================================
i = 232411
j = 122198
fh_spectrum = open('spectrum.spe','w')
single(fh_real,fh_global,fh_spectrum,i, j)
fh_spectrum.close()

#values, counts = np.unique(mx_spec, return_counts=True)
unique_words = set(mx_spec)
u_list = list(unique_words)    
m = len(u_list)
n = len(mx_spec)

print(str(n)+" "+str(m))
many = np.zeros(10000)
xmax = 0
fh_tot = open('unique.spe','w')
for i in range(0,m):
    x = sumList(u_list[i])
    many[int(x)] += int(1)
    if x > xmax:
        xmax = x
    xtemp = 'SUM_'+ str(x)
    fh_tot.write(u_list[i]+' ['+str(x)+']\n')
    temp = u_list[i].replace(" ","_")
    createTriple(fh_global,str(temp), 'type', 'Relation', 0,classUri,classUri,classUri,'void')
    createTriple(fh_global,str(xtemp), 'type', 'Sum', 0,classUri,classUri,classUri,'void')
    createTriple(fh_global,str(temp), 'hasSum', str(xtemp), 0,classUri,classUri,classUri,'void')
    family(x,u_list[i])
fh_tot.close()

print("XMAX="+str(xmax))
for i in range(0,xmax):
    xtemp = 'SUM_'+ str(i)
    createTriple(fh_global,str(xtemp), 'noOfLiterals', str(int(many[i])), 1,classUri,classUri,classUri,'integer')

fh_global.close()
fh_real.close()
#============================================================
# End of File
#============================================================