import numpy as np
import pandas as pd
import chatalyticsengine as c
import matplotlib.pyplot as plt
from datetime import timedelta

data = c.loadData("private/full_test_data.txt")
print(data)

x = np.arange(pd.to_datetime(data.index[data["index"] == 0]), pd.to_datetime(data.index[data["index"] == data.shape[0] - 1]), step=timedelta(days=1))
fx = x

fig, ax = plt.subplots()
ax.plot(x, fx)  

ax.set(xlabel='x', ylabel='y', title='title')
ax.grid()

plt.show()

