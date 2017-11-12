import sys

flist=['imVkohli_tweets.csv']


def clean_file(fl):
    fp = open(fl,'r')
    exc=[]
    for line in fp:
        #print line
        if '#' in line:
            try:
                print line.split(',')[2]
            except:
                exc.append(line)
    print exc

if __name__=='__main__':
    for fl in flist:
        clean_file(fl);
