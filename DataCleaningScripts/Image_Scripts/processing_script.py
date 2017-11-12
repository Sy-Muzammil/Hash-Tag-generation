import os
from shutil import copyfile

curdir = os.path.dirname(os.path.realpath(__file__))
datadir=curdir+"/../ImageCorpus1/"
outdir=curdir+"/sel_images/"
cnt=0
flist = os.listdir(datadir)
for j in flist:
    print j
    if os.path.getsize(datadir+j) > 0:
        copyfile(datadir+j,outdir+j)
        cnt+=1
        if cnt>120000:
            break
print cnt
