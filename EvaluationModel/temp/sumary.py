import sys

d_good={}
d_bad={}
f=open(sys.argv[1],'r')
for line in f:
    data= line.split('|')
    # print data[1],data[2]
    d_good[data[2]]=float(data[1])
f=open(sys.argv[2],'r')
d_bad['DropCatch.com']=0
for line in f:
    data=line.split('|')
    if data[2].find("DropCatch.com") != -1:
        d_bad['DropCatch.com']+=float(data[1])
    else:
        d_bad[data[2]]=float(data[1])
# for key in d_good:
    # print key.strip()
    # print d_good[key]
for key in d_bad:
    # print key.strip()
    print d_bad[key]
# print d_good,d_bad
