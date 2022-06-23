import numpy as np
import ChatalyticsEngine as c
from datetime import datetime
import matplotlib.pyplot as plt

# GET CELL: data.loc[y, x]

data = c.loadData("private_test_data1.txt")

print(data)

x = np.arange(np.datetime64('2022-06-05'), np.datetime64('2022-06-22'), np.timedelta64(1, 'D'))
fx = np.random.randn(len(x))

fig, ax = plt.subplots()
ax.plot(x, fx)  

ax.set(xlabel='x', ylabel='y', title='title')
ax.grid()

plt.show()
