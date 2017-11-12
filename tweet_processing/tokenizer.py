#!/usr/bin/env python
# -*- coding=utf-8 -*-

from __future__ import division, unicode_literals
import sys
import io
import re
import os
import string
import codecs
import time

class Tokenizer:
    
    def __init__(self):
        self.punctuation = set(string.punctuation)
        file_path = os.path.dirname(os.path.abspath(__file__))
        with io.open('%s/data/EMOTICONS' % file_path, encoding='utf-8') as fp:
            self.emoticons = set(fp.read().split())
        # List of Non-breaking Prefixes
        with io.open('%s/data/NONBREAKING_PREFIXES' % file_path, encoding='utf-8') as fp:
            self.NBP = set(fp.read().split())
        with io.open('%s/data/DOMAINS' % file_path, encoding='utf-8') as fp:
            self.domains = set(fp.read().split())
        self.pemos = set([x for x in self.emoticons if 
                    (any(c in self.punctuation for c in x) and all(ord(c)<256 for c in x))]) 
        self.NBP = self.NBP.union(set(string.ascii_letters[:26]))
        self.NBP_NUM = set(['No', 'no', 'Art', 'pp'])
        self.contractions = """ 'all 'am 'clock 'd 'll 'm n't
                            're 's 'sup 'tis 'twas 've 'n' """
        self.contractions = self.contractions.split() +\
            self.contractions.upper().split()

        self.isurl = re.compile(r'[a-z][a-z][.][a-z][a-z]').search 
        self.joints = re.compile(r'(^[A-Za-z][A-Za-z]+)[.]'
                                 r'([A-Za-z][A-Za-z]+$)')
        self.restoredots = re.compile(r'(DOT)(\1*)MULTI')
        self.umathop = re.compile('([\u2200-\u2211\u2213-\u22ff])')
        self.ucurrency = re.compile('([\u20a0-\u20cf])')
        self.specascii = re.compile(r'([\\!$%^&*()_+={\[}\]|";:<>?`~/])')    
        self.multidot = re.compile(r'(\.\.+)([^\.])')
        self.notanumc = re.compile('([^0-9]),')
        self.cnotanum = re.compile(',([^0-9])')
        self.numcs = re.compile("([0-9])'s")
        self.aca = re.compile("([a-zA-Z])'([a-zA-Z])")
        self.acna = re.compile("([a-zA-Z])'([^a-zA-Z])")
        self.nacna = re.compile("([^a-zA-Z])'([^a-zA-Z])")
        self.rpunct = re.compile(r'[.,\\!@#$%^&\'*()_+={\[}\]|";:<>?`~/]')


    def normalizePunctuations(self, line):
        line = re.sub('[\u2010\u2043]', '-', line)  # hyphen
        line = re.sub('[\u2018\u2019]', "'", line)  # single quotes
        line = re.sub('[\u201c\u201d]', '"', line)  # double quotes
        return line


    def unmask_emos_urls(self, text):
        text = text.split()
        for i, token in enumerate(text):
            if token.startswith('eMoTiCoN-'):
                emo_id = int(token.split('-')[1])
                text[i] = self.emos_dict[emo_id]
            elif token.startswith('sItEuRl-'):
                url_id = int(token.split('-')[1])
                text[i] = self.url_dict[url_id]
                #text[i] = 'U-R-L'
        return ' '.join(text)

    def mask_emos_urls(self, text):
        n_e, n_u = 0, 0
        text = re.sub(r'([\W_])(http://|https://|www.)', r'\1 \2', text)
        self.url_dict = dict()
        self.emos_dict = dict()
        words = text.split()
        text = []
        for wd in words:
            if any(c in self.punctuation for c in wd) and len(wd) > 2:
                for em in self.pemos:
                    br = len(em)
                    if wd.startswith(em):
                        wd = '%s %s' %(wd[:br], wd[br:])
                    if wd.endswith(em):
                        wd = '%s %s' %(wd[:-br], wd[-br:])
            text.append(wd)
        text = ' '.join(text).split()
        for i, token in enumerate(text):
            if token in self.emoticons:
                text[i] = 'eMoTiCoN-%d' % n_e
                self.emos_dict[n_e] = token
                n_e += 1
                continue
            is_url = False
            if (token.startswith('http://') or
                token.startswith('https://') or
                    token.startswith('www.')):
                is_url = True
            elif self.isurl(token):
                tokens = self.rpunct.split(token)
                is_url = any(x in self.domains for x in tokens[1:])
            if is_url:
                t2 = ''
                if token[-2:] == "'s":
                    t2 = "'s"
                    token = token[:-2]
                elif token[-1] in ",.!?;:'\"":
                    t2 = token[-1]
                    token = token[:-1]
                text[i] = 'sItEuRl-%d' % n_u
                self.url_dict[n_u] = '%s %s' % (token, t2)
                n_u += 1
                continue
        text = ' '.join(text)
        text = ' %s ' % (text)
        return text    

    def normalize(self, line):
       line =  self.normalizePunctuations(line)
       return line

    def tokenizer(self,text):
        #text = ' %s ' % (text)
        text = text.decode('ascii',errors='ignore')
        text = self.mask_emos_urls(text)
        text = self.umathop.sub(r' \1 ', text)
        text = self.ucurrency.sub(r' \1 ', text)
        text = self.specascii.sub(r' \1 ', text)
        text = self.multidot.sub(lambda m: r' %sMULTI %s' % (
            'DOT' * len(m.group(1)), m.group(2)), text)
        text = self.notanumc.sub(r'\1 , ', text)
        text = self.cnotanum.sub(r' , \1', text)
        text = self.nacna.sub(r"\1 ' \2", text)
        text = self.acna.sub(r"\1 ' \2", text)
        text = self.aca.sub(r"\1 '\2", text)
        text = self.numcs.sub(r"\1 's", text)
        text = re.sub(r' (\.+)([^0-9])', r' \1 \2', text)
        text = self.unmask_emos_urls(text)
        return text.split()
    
    def tokenize_prefixes(self, text):
        words = text
        text_len = len(words) - 1
        text = str()
        for i, word in enumerate(words):
            if word[-1] == '.':
                dotless = word[:-1]
                if dotless.isdigit():
                    word = dotless + ' .'
                elif (('.' in dotless and re.search('[a-zA-Z]', dotless)) or
                        dotless in self.NBP):
                    pass
                elif (dotless in self.NBP_NUM and
                      (i < text_len and words[i + 1][0].isdigit())):
                    pass
                #elif i < text_len and words[i + 1][0].isdigit():
                #    pass
                else:
                    word = dotless + ' .'
            elif self.joints.search(word):
                w1, w2 = word.split('.')
                if word in self.NBP:
                    pass
                elif w1 in self.NBP:
                    word = '%s. %s' % (w1, w2)
                else:
                    word = '%s . %s' % (w1, w2)
            text += "%s " % word
        return ' %s ' % text

if __name__ == "__main__" :
    INFilePath = sys.argv[1]
    #OUTFilePath = sys.argv[1]
    OUTFilePath = open(sys.argv[2],'w')
    FileList = []
    start_time = time.time()
    TK = Tokenizer() 
    with open(INFilePath) as fp:
        for line in fp:
            norm = TK.normalize(line)
            tokSen = TK.tokenizer(norm)
            sentence = TK.tokenize_prefixes(tokSen)
            text = TK.restoredots.sub(lambda m: r'.%s' %('.' * int((len(m.group(2)) / 3))),sentence)
            OUTFilePath.write(text.encode("utf-8") + "\n")
    fp.close()
    OUTFilePath.close()
    elapsed_time = time.time() - start_time
    print('Took {:.03f} seconds'.format(elapsed_time))

    
        
        