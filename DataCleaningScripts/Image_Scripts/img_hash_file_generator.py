import os

curdir = os.path.dirname(os.path.realpath(__file__))
datadir = curdir+"/../Imagehash/"
imdir = curdir+"/sel_images/"
flist = os.listdir(datadir)
ofl = "sel_img_hash_ind.txt"
ofd = open(ofl,'w')

imdict={}
for l in os.listdir(imdir):
    #print l.split(".")[0]
    imdict[l.split(".")[0]] ="-1"
    
print len(imdict)
    
cnt=0
for fl in flist:
    fp = open(datadir+fl,'r')
    for j in fp:
        parts = j.split('\t')
        if parts[0] in imdict and imdict[parts[0]]=='-1':
            #print parts[0]
            imdict[parts[0]] = "0"
            cnt+=1
            ofd.write(j)
    fp.close()
ofd.close()
