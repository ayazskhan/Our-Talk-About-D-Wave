#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Copyright 2020 Alex Khan
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Things to do:
 - Please name this file <demo_name>.py
 - Fill in [yyyy] and [name of copyright owner] in the copyright (top line)
 - Add demo code below
 - Format code so that it conforms with PEP 8
"""

import numpy as np
from numpy.random import rand

from dwave.system.samplers import DWaveSampler
from dwave.system.composites import EmbeddingComposite
from minorminer import find_embedding
import networkx as nx
import dwave.inspector
import pandas as pd

# Option 1 Generate Matrix 
#dim=50
#Q =  2*rand(dim,dim) - 1
#Q = (Q+Q.T)/2
#for k in range(dim):
#    Q[k,k] = np.abs(Q[k,k])

# Option 2 Load Matrix

Q = pd.read_csv("Q30.csv").values
dim=len(Q[0])

print(Q)

# convert matrix into a QUBO with linear=biases and quadratic=couplings terms
linear={('a'+str(k), 'a'+str(k)):Q[k][k] for k in range(dim)}

quadratic={('a'+str(i+1), 'a'+str(j)):Q[i+1][j] for i in range(dim-1) for j in range(dim-1) if j<i+1}

QDwave = dict(linear)
QDwave.update(quadratic)

print(QDwave)

chainstrength = 1
numruns = 10

sampler = EmbeddingComposite(DWaveSampler())


response = sampler.sample_qubo(QDwave, chain_strength=chainstrength, num_reads=numruns)
#print(response)
#print(response.data)

# print qubits with value 1
best=0
for sample, energy, n_occurences, chain_break_freq in response.data():
    sample_list=[]
    for a in range(dim):
        #sample_str.append(str(sample['a'+str(a)]))
        if sample['a'+str(a)]==1:
            sample_list.append(a)
    if best==0:
        best_DWave_val='best D-Wave:'+str(sample_list)+' energy:'+str(energy)+' occurences:'+str(n_occurences)
        best=1
    print(sample_list, energy, n_occurences)
print(best_DWave_val) 

dwave.inspector.show(QDwave,response)






