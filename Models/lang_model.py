# https://github.com/spro/char-rnn.pytorch

import torch
import torch.nn as nn
from torch.autograd import Variable

class LangModel(nn.Module):
    def __init__(self, input_size, hidden_size, output_size, model="lstm", n_layers=1):
        super(LangModel, self).__init__()
        self.model = model.lower() # for the sake of the correctns.
        self.input_size = input_size # to be learnt
        self.hidden_size = hidden_size
        self.output_size = output_size
        self.n_layers = n_layers

        self.encoder = nn.Embedding(input_size, hidden_size)
        if self.model == "gru":
            self.rnn = nn.GRU(hidden_size, hidden_size,1)
        elif self.model == "lstm":
            self.rnn = nn.LSTM(hidden_size, hidden_size,1)
        self.decoder = nn.Linear(hidden_size, output_size)

    def forward(self, inp):
        batch_size = inp.size(0)
        hidden = self.init_hidden(batch_size)
        encoded = self.encoder(inp)
        temp  = encoded.view(1,batch_size,-1)
        output, self.hidden = self.rnn(temp, hidden)
        output = self.decoder(output.view(batch_size, -1))
        return output, hidden

    def init_hidden(self, batch_size):
        if self.model == "lstm":
            return (Variable(torch.zeros(self.n_layers, batch_size, self.hidden_size)),
                    Variable(torch.zeros(self.n_layers, batch_size, self.hidden_size)))
        return Variable(torch.zeros(self.n_layers, batch_size, self.hidden_size))
input_size = 1024
hidden_size = 400
num_layers = 10
output_size = 52
model = LangModel(input_size,hidden_size,output_size)
a = Variable(torch.zeros(1024).long())
h1 = (Variable(torch.zeros(1, 1,400)),
                    Variable(torch.zeros(1, 1, 400)))
out1,h1 = model(a)