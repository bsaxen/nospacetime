import matplotlib.pyplot as plt

xv = []
yv = []
fh_in = open('real.txt','r')
count = 0
for line in fh_in:
    count += 1
    line = line.replace("\n","")
    sp = line.split(" ")
    x = sp[0]
    y = sp[1]
    if count < 60000:
        print(str(count)+' '+str(x)+" "+str(y))
        xv.append(float(x))
        yv.append(float(y))
fh_in.close()

#plt.plot(xv,yv)
plt.scatter(xv,yv,s=1)
plt.ylabel('zum')
plt.show()