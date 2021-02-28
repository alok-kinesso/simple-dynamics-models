import numpy as np
import matplotlib.pyplot as plt

# initial values
b = 0.0
i = 0.001
o = 0.0

# parameters
## O-decay
k = 0.85
## IO-lag
T = 2
state = [{"b": b, "i": i, "o": o}]*T
## IB-sigmoid
### https://www.desmos.com/calculator/htwayvkmsc
### <iframe src="https://www.desmos.com/calculator/jkkpiyy3nf?embed" width="500px" height="500px" style="border: 1px solid #ccc" frameborder=0></iframe>
### https://www.desmos.com/calculator/jkkpiyy3nf
scale = 10
shift = 0.25
# replication
replication = 1.5
# transition functions
def next_b(state, scale=scale, shift=shift):
  i = state[-1]["i"]
  return 1.0/(1.0 + np.exp(-1.0*scale*(np.tan(np.pi*(np.power(i,shift)) - np.pi/2))))

def next_i(state, R=replication):
  i = state[-1]["i"]
  o = state[-1]["o"]
  s = 1.0 - (i+o) # s + i + o = 1.0
  at_risk = s*(R-b)
  return at_risk*i

def next_o(state, decay=k):
  o = state[-1]["o"]
  ip = state[0]["i"]
  return min(k*o + ip, 1.0)

infections = []
behaviors = []
for t in range(100):
  next_vector = {"b": next_b(state), "i": next_i(state), "o": next_o(state)}
  state.append(next_vector)
  state = state[1:]
  if not t % 80:
    print(t, '\t', next_vector)
  infections.append(next_vector["i"])
  behaviors.append(next_vector["b"])

x = range(len(infections))
# fig = plt.figure()
# ax = fig.add_subplot(2, 1, 1)
#ax.set_ylim([0.0, 1.0])
#ax.set_yscale('log')

fig,ax = plt.subplots()
ax.plot(x, infections, label='infections', color='red')
ax.set_ylabel("infections",color="red",fontsize=14)
ax.set_xlabel("weeks",fontsize=14)
ax2=ax.twinx()
ax2.plot(x, behaviors, label='behaviors', color='blue')
ax2.set_ylabel("behaviors",color="blue",fontsize=14)
fig.legend()
plt.title('pay attention to y-axis values!')
plt.savefig('timeseries.png', dpi=90)

fig,ax=plt.subplots()
ax.plot(infections, behaviors)
ax.set_xlabel("infections",fontsize=14)
ax.set_ylabel("behaviors",fontsize=14)
plt.title('behavior dependence on infections')
plt.savefig('behavior_against_infections.png', dpi=90)
