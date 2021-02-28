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
def b(state, scale=scale, shift=shift):
  i = state[-1][2]
  return 1.0/(1.0 + np.exp(-1.0*scale*(np.tan(np.pi*(np.power(i,shift)) - np.pi/2))))

def i(state, R=replication):
  s = 1.0 - (state[-1][1]+state[-1][2]) # s + i + o = 1.0
  at_risk = s*(R-b)
  return at_risk*i

def o(state, decay=k):
  o = state[-1][-1]
  ip = state[0][2]
  return np.min(k*o + ip, 1.0)

for t in range(20):
  new_vector = [b(state), i(state), o(state)]
  state += new_vector
  state = state[1:]
  print(new_vector)
