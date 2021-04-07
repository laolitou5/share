import matplotlib.pyplot as plt
import random

position=0
walk=[]
steps=500
for i in range(steps):
    step=1 if random.randint(0,1) else -1
    position+=step
    walk.append(position)
print(walk)
fig=plt.figure()
ax=fig.add_subplot(211)
ax.plot(walk)

ax=fig.add_subplot(223)
ax.plot(walk)

ax=fig.add_subplot(224)
ax.plot(walk)
plt.show()