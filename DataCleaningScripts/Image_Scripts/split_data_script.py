infl = "sel_img_hash_ind.txt"
imgfl="names_lno.txt"
labels="labels.txt"

inpfd = open(infl,'r')
imfd=open(imgfl,'w')
lblfd=open(labels,'w')

def process_hashtags(inp):
    hashes = inp.split()
    ret =""
    for k in hashes:
        ret += "# "
        for j in k:
            ret += j+" "
    ret +="\n"
    return ret

cnt=0
for j in inpfd:
    parts = j.split("\t",1)
    imfd.write(parts[0]+".jpg"+" "+str(cnt)+"\n")
    processed_label = process_hashtags(parts[1])
    lblfd.write(processed_label)
    cnt +=1
