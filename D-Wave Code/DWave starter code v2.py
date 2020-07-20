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

# Random matrix
dim=20
Q =  2*rand(dim,dim) - 1
Q = (Q+Q.T)/2
for k in range(dim):
    Q[k,k] = np.abs(Q[k,k])

#Problem -> Solution
# Creating a formula that is in this qubit adder formulation 
# QUBO - Quadratic Unconstrained Binary Optimization
# Balance your QUBO

# Example
#[[ -0.11209597 -0.005184097]
# [             0.05494179]]

# Solve your problem here
# Create a matrix that represents the problem
# Submit the matrix to DWave
print(Q)
# convert matrix into a QUBO with linear=biases and quadratic=couplings terms
linear={('a'+str(k), 'a'+str(k)):Q[k][k] for k in range(dim)}

quadratic={('a'+str(i+1), 'a'+str(j)):Q[i+1][j] for i in range(dim-1) for j in range(dim-1) if j<i+1}

QDwave = dict(linear)
QDwave.update(quadratic)

print(QDwave)

chainstrength = 10
numruns = 10

#clique = nx.complete_graph(7).edges()
#target_graph = nx.random_regular_graph(d=4, n=30).edges()
#embedding = find_embedding(clique, target_graph)
#print(embedding)

sampler = EmbeddingComposite(DWaveSampler())


response = sampler.sample_qubo(QDwave, chain_strength=chainstrength, num_reads=numruns)
print(response)
dwave.inspector.show(QDwave,response)

#         a0           a1         a2          a3         a4
# a0 [[ *0.91199117 -0.24116519 -0.20609761 -0.6630097   0.44338965]
# a1 [-0.24116519  *0.25892196  0.11011308 -0.08535894 -0.47754192]
# a2 [-0.20609761  0.11011308  *0.30821145 -0.01814748  0.66982811]
# a3 [-0.6630097  -0.08535894 -0.01814748  *0.2377746  -0.39323481]
# a4 [ 0.44338965 -0.47754192  0.66982811 -0.39323481  *0.47625565]]


# In[ ]:




