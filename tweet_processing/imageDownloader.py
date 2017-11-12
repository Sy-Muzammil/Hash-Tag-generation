import os
import urllib
import threading
import urllib2
import time
from threading import Lock
lock = Lock()
#path1 = '/home/group3/processData/Image_processing/Imagefile/'
#path = '/home/group3/processData/Image_processing/'
path1='/home/muzammil/Desktop/IRE_MAJOR/tweet_processing/'
mydict = {}
#for file in os.listdir(path1):
#       	filename = file.split(".")[0]
#        if file.endswith(".txt"):
 #               print filename
with open(path1  +"image.txt",'r') as fp:
	for line in fp:
		key = line.split("\t")[0]
		mydict[key] = line.split("\t")[1]
		#for key, value in mydict.iteritems():
		#	resource = urllib.urlopen(value)
		#	output = open(path+ "ImageCorpus/"+key+".jpg","wb")
		#	output.write(resource.read())
		#	output.close()


start = time.time()

def fetch_url(key,value):
	resource = urllib.urlopen(value)
	lock.acquire()
	output = open(path1+ "imagefolder/"+key+".jpg","wb")
	output.write(resource.read())
	output.close()
	lock.release()
    	print "'%s\' fetched in %ss" % (value, (time.time() - start))

threads = [threading.Thread(target=fetch_url, args=(key,value,)) for key,value in mydict.iteritems()]
cnt = 0;
for thread in threads:
    cnt+=1
    thread.start()
    if cnt == 20:
	time.sleep(5)
    	cnt = 0
for thread in threads:
    thread.join()

print "Elapsed Time: %s" % (time.time() - start)

