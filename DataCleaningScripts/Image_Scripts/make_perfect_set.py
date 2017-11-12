import os
from shutil import copyfile

curdir = os.path.dirname(os.path.realpath(__file__))
fl = "sel_img_hash_ind.txt"
fp = open(fl,'r')
fdict={}




for j in fp:
    fn = j.split("\t")[0]
    fdict[fn]=1
fp.close()

cnt=0
imglist = os.listdir(curdir+"/sel_images/")
for j in imglist:
    if j.split(".")[0] in fdict:
        copyfile(curdir+"/sel_images/"+j,curdir+"/perfect_set/"+j)

