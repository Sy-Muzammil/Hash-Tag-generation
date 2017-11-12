import csv
import re
import string
from wordsegment import load, segment
#from findwords import SplitIntoWords
from collections import defaultdict
from tokenizer import Tokenizer
path = '/home/muzammil/Desktop/IRE_MAJOR/tweet_processing/'

TK = Tokenizer()
#FN = SplitIntoWords()
load()
class Processsing:
	
	def __init__(self):
		self.Tweet_dict = {}
		self.Text_dict = {}
		self.hash_dict = defaultdict(list)
		self.Image_dict = {}
		self.endofsent =[]
		self.link = re.compile('(http.*?\s?).*', re.DOTALL)
		self.endofsent.append(self.link)
		for i in string.punctuation:
			if i != ",":
				self.endofsent.append(i)
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

		for key, value in self.Tweet_dict.iteritems():
			#text = value
			words = []
			flag  = 0
			norm = TK.normalize(value)
			tokSen = TK.tokenizer(norm)
			sentence = TK.tokenize_prefixes(tokSen)
			text = TK.restoredots.sub(lambda m: r'.%s' %('.' * int((len(m.group(2)) / 3))),sentence)
			text = text.encode("utf-8")
			for word in text.split():
				word = word.strip()
				if word:
					if word[0] == '#':
						leng = len(words)
						if leng > 0 and words[leng-1] in self.endofsent:
							temp = segment(word)
							word = " ".join(temp)
							self.hash_dict[key].append(word)
							flag = 1;
						else:
							words.append(word[1:]) 
					else:
						if '@' in word:
							word = word.replace('@',"")
						words.append(word)
			if flag == 1:
				self.Text_dict[key] =  ' '.join(words)
			else:
				continue

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

    