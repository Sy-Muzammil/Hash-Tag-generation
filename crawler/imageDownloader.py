import urllib
import os
path1 = '/home/group3/processData/Image_processing/Imagefile/'
path = '/home/group3/processData/Image_processing/'
mydict = {}
IDs = {}
for file in os.listdir(path1):
       	filename = file.split(".")[0]
        if file.endswith(".txt"):
                print filename
		with open(path1 + filename+'.txt','r') as fp:
			for line in fp:
				key = line.split("\t")[0]
				mydict[key] = line.split("\t")[1]
		for key, value in mydict.iteritems():
			resource = urllib.urlopen(value)
			output = open(path+ "ImageCorpus/"+key+".jpg","wb")
			output.write(resource.read())
			output.close()
