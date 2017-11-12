import csv
import re
from collections import defaultdict

path = '/home/muzammil/Desktop/IRE_MAJOR/tweet_processing/'

class Processsing:
	
	def __init__(self):
		self.Tweet_dict = {}
		self.Text_dict = {}
		self.hash_dict = defaultdict(list)
		self.Image_dict = {}
		self.getitems()

	def getitems(self):
		
		file=open( path +"zem_tweets.csv", "r")
		reader = csv.reader(file)
		reader.next()
		for line in reader:
		    self.Tweet_dict[line[0]] = line[2]
		    self.Image_dict[line[0]] = line[3]
		
		# for key, value in self.Tweet_dict.iteritems():
		# 	print key," => ",value

	def strip_links(self):
		for key, value in self.Tweet_dict.iteritems():
			text = value
			#print "1: ",text
			link_regex    = re.compile('(http.*?\s?).*', re.DOTALL)
			links         = link_regex.search(text)
			if links:
				text = text.replace(links.group()," ")
			#print "2: ", text
			self.Tweet_dict[key] = text.strip()


	def strip_all_entities(self):
		entity_prefixes = ['@','#']
		

		for key, value in self.Tweet_dict.iteritems():
			text = value
			words = []
			for word in text.split():
				word = word.strip()
				if word:
					if '@' in word:
						continue
					elif word[0] == '#':
						self.hash_dict[key].append(word) 
					else:
						words.append(word)
			self.Text_dict[key] =  ' '.join(words)
		# for key, value in self.Image_dict.iteritems():
		# 	print key," => ",value

	def writeInFiles(self):
		textfile = open(path+'text.txt','w+')
		hash_file = open(path+'hash.txt','w+')
		imagefile = open(path+'image.txt','w+')
		for key, value in self.Image_dict.iteritems():
			imagefile.write(key+"\t"+value+"\n")
		for key, value in self.hash_dict.iteritems():
			hashs = '\t'.join(value)
			hash_file.write(key+"\t"+hashs+"\n")
		for key, value in self.Text_dict.iteritems():
			textfile.write(key+"\t"+value+"\n")

if __name__ == '__main__':
	Pr = Processsing()
	Pr.strip_links()
	Pr.strip_all_entities()
	Pr.writeInFiles()
    