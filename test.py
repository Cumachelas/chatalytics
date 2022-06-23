import chatalyticsengine as c
import pandas as pd
import numpy as np
from datetime import timedelta

# Load data from .txt to DataFrame
data = c.loadData("private/full_test_data.txt")
print(data)

# Get data or specific column from Timestamp
new_data = data.loc["2022-12-04", "sender"]
new_data = data.loc["2022"]

# Get data or specific column from time range and the number of messages
new_data = data.loc["2020-09-09T00:00":"2020-09-09T23:59"]
n = len(new_data)

# Get data based on a condition
new_data = data[data["index"] == 69]
n = len(new_data)

# Get indexes (dates) of rows where a condion is met
dates = data.index[data["message"] == "Ja"].tolist()

# Get date of the first and last message in data
dt0 = pd.to_datetime(data.index[data["index"] == 0])
dt1 = pd.to_datetime(data.index[data["index"] == data.shape[0] - 1])


x = pd.date_range(dt0.to_pydatetime(), dt1.to_pydatetime())

print(x)