from collections import OrderedDict
import numpy as np
import ChatalyticsEngine as c
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

# GET CELL: data.loc[y, x]

data = c.loadData("private_test_data1.txt")
    
#print(len(c.daterange(data, datetime(2022, 6, 10, 0, 0, 0), datetime(2022, 6, 11, 0, 0, 0))))

#list_of_dates = []
#list_of_dates = [d.date() for d in data["timestamp"].tolist()]
#no_duplicates = list(OrderedDict.fromkeys(list_of_dates))

x = np.arange(data["timestamp"].iloc[0], data["timestamp"].iloc[data.shape[0]-1], step=timedelta(days=1))
fx = c.daterange(data, x, x + np.arange(timedelta(hours=23, minutes=59)))

plt.plot(x, fx)

plt.grid()

plt.show()

# LIST Dates -> leave YMD -> get rid of duplicates
