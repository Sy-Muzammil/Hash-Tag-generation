
# coding: utf-8

# In[48]:


from torch import autograd

fname = 'text.txt'

def read_seq_from_file(filename):
    fp  = open(filename,'r')
    ret=[]
    for line in fp:
        line = line.split('\t')[1]
        ret.append(line)

    fp.close()
    return ret


# In[49]:


def prepare_sequence(seq, to_ix, cuda=False):
    lis=[]
    for w in seq.split():
        if w in to_ix:
            lis.append(to_ix[w])
        else:
            lis.append(to_ix['<unk>'])
    var = autograd.Variable(torch.LongTensor(lis))
    return var,lis


# In[50]:


import torch 
import torch.nn as nn
import numpy as np
from torch.autograd import Variable
from data_utils import Dictionary, Corpus
import re

# Hyper Parameters
embed_size = 100
hidden_size = 1024
num_layers = 5
num_epochs = 5
num_samples = 1000   # number of words to be sampled
batch_size = 20
seq_length = 15 
learning_rate = 0.002

# Load Penn Treebank Dataset
train_path = './data/train.txt'
sample_path = './sample.txt'
#print ids
#vocab_size = len(corpus.dictionary)
#num_batches = ids.size(1) // seq_length

#Custom variables
glove_embeddings_file = "glove.twitter.27B.100d.txt"
text_file_name = "text.txt"


# In[51]:


def load_word2vec(file):
    word2vec = []
    iddict = {}
    fin= open(file)
    cnt=0   
    for line in fin:
                items = line.split(' ')
                word = items[0]
                vect = np.array([float(i) for i in items[1:] if len(i) > 1])
                if(len(vect)!=100):
                    continue
#                 print len(vect)
                iddict[word] = cnt
                word2vec.append(vect)
    # 	            cnt=cnt+1
    # 	            if cnt%100000==0:
    # 	            	print cnt/100000
    return word2vec,iddict


# In[ ]:


twtfilename = "Glove/glove.twitter.27B.100d.txt"

id_to_embed,word_to_id = load_word2vec(twtfilename)




# In[ ]:



import numpy as np
mapping = torch.Tensor(id_to_embed)
# for i in range(0,len(id_to_embed)):
#     if len(id_to_embed[i])!=100:
#         print i
#     for j in range(0,100):
#         mapping[i][j]=id_to_embed[i][j]
print type(mapping)


# In[52]:


# glove_embed_dict = load_word2vec(glove_embeddings_file)
vocab_size = mapping.size(0)
print vocab_size


# In[58]:




# RNN Based Language Model
class RNNLM(nn.Module):
    def __init__(self, vocab_size, embed_size, hidden_size, num_layers,embeddings):
        super(RNNLM, self).__init__()
        self.embedding = nn.Embedding(embeddings.size(0), embeddings.size(1))
        self.embedding.weight = nn.Parameter(embeddings)
        self.lstm = nn.LSTM(embed_size, hidden_size,5)
        self.linear = nn.Linear(hidden_size, vocab_size)
#         self.init_weights()
        
    def init_weights(self):
        self.linear.bias.data.fill_(0)
        self.linear.weight.data.uniform_(-0.1, 0.1)
        
    def forward(self, sentence, h):
        # Embed word ids to vectors
        embeds = self.embedding(sentence)
        x = embeds.view(len(sentence), 1, -1)

        lstm_out, h = self.lstm(x, h)
         
        return lstm_out[-1]


# In[59]:


print type(id_to_embed)
seq_list = read_seq_from_file(fname)
# mat = []
# retvar
# pllist
for l in seq_list:
    retvar,pllist = prepare_sequence(l,word_to_id)
#     mat.append(retvar)
batch_size = 5 #basically the number of.
model = RNNLM(vocab_size, embed_size, hidden_size, num_layers,mapping)
# print "final mat size ",len(mat)

    # Initial hidden and memory states
states = (Variable(torch.zeros(5, 1, hidden_size)),
          Variable(torch.zeros(5, 1, hidden_size)))


# In[ ]:


# print type(retvar)
# # inp = torch.from_numpy(np.ndarray(mat))
# print retvar.size()
# input_to_model = Variable(inp[:,1,:])
# print input_to_model


# In[63]:


# test = Variable(inpuy)
retvar = [1,2,3,4,5,6,7,8,9,20,21]
dum = Variable(torch.from_numpy(np.array(retvar)))
output = model(dum,states)


# In[64]:


print output


# In[38]:


embedding = nn.Embedding(mapping.size(0), mapping.size(1))
embedding.weight = nn.Parameter(mapping)
lstm = nn.LSTM(embed_size, hidden_size,5)
linear = nn.Linear(hidden_size, vocab_size)
# init_weights()

embeds = embedding(dum)
x = embeds.view(len(dum), 1, -1)


# In[40]:



print x.size()
lstm_out, states = lstm(x, states)


# In[61]:


# states
states = (Variable(torch.zeros(5, 1, hidden_size)),
          Variable(torch.zeros(5, 1, hidden_size)))


# In[45]:


print lstm_out[-1]

