import ChatalyticsEngine as c
from datetime import datetime

data = c.loadData("private/full_test_data.txt")

print(str(data) + "\n\n")

date1 = datetime.strptime("10.9.2020", "%d.%m.%Y")
date2 = datetime.strptime("12.9.2020", "%d.%m.%Y")

print(c.daterange(data, date1, date2))