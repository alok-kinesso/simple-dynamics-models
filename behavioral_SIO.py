import numpy as np
# initial values
b = 0.0
i = 0.0001
o = 0.0

# parameters
## O-decay
k = 0.9
## IO-lag
T = 2
state = [[b,i,o]]*T
## IB-sigmoid
### https://www.desmos.com/calculator/htwayvkmsc
### <iframe src="https://www.desmos.com/calculator/jkkpiyy3nf?embed" width="500px" height="500px" style="border: 1px solid #ccc" frameborder=0></iframe>
### https://www.desmos.com/calculator/jkkpiyy3nf
scale = 10
shift = 0.33
# replication
replication = 2.0
# transition functions
def next_b(state, scale=scale, shift=shift):
  i = state[-1][2]
  return 1.0/(1.0 + np.exp(-1.0*scale*(np.tan(np.pi*(np.power(i,shift)) - np.pi/2))))

def next_i(state, R=replication):
  s = 1.0 - (state[-1][1]+state[-1][2]) # s + i + o = 1.0
  at_risk = s*(R-b)
  return at_risk*i

def next_o(state, decay=k):
  o = state[-1][-1]
  ip = state[0][2]
  return np.min(k*o + ip, 1.0)

for t in range(20):
  next_vector = [next_b(state), next_i(state), next_o(state)]
  state += next_vector
  state = state[1:]
  print(next_vector)
