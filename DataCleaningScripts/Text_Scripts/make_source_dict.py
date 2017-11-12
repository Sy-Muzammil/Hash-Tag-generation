import sys

flist = ['X_dev.txt','X_test_fin.txt','X_train_fin.txt']
oflist = ['dev_output.txt','test_output.txt','train_output.txt']
yflist = ['Y_dev.txt','Y_test_fin.txt','Y_train_fin.txt']

gdict={}
cnt=0;
nlin=0
esc_list=["\n"," ","\t"]
fr = open("vocab.source",'w')
for fl in flist:
    fd = open(fl,'r')
    for line in fd:
        nlin+=1
        parts = line.split(":",1)
        parts = parts[0].split(" ");
        for k in parts:
            if (k not in esc_list) and  (k not in gdict) :
                print k
                fr.write(k+"\n")
                gdict[k] = cnt
                cnt+=1;
    fd.close()
fr.close()
#print "The number of lines ",nlin

#generating the main file.
for j in range(3):
    text=[]
    tags=[]
    infl = flist[j]
    htgfl = yflist[j]
    ofl = oflist[j]
    infd = open(infl,'r')
    htfd = open(htgfl,'r')
    for l in infd:
        text.append(l)
    for l in htfd:
        tags.append(l)
    infd.close()
    htfd.close()
    ofd = open(ofl,'w')
    for num in range(len(text)):
        line = text[num]
        line = line.split(":",1)
        line = line[0].split(" ")
        for k in line:
            if k in gdict:
                ofd.write(str( gdict[k])+" ")
        ofd.write("\t")
        hash_string = tags[j]
        for c in tags[j]:
            if ord(c) <=ord('z') and ord(c) >=ord('a'):
                ofd.write(str(ord(c)-ord('a')+10)+" ")
            if ord(c)<=ord('9') and ord(c)>=ord('1'):
                ofd.write(str(ord(c)-ord('1'))+" ")
            if ord(c)==32:
                ofd.write(str(36)+" ")
        ofd.write("\n")
    ofd.close()
