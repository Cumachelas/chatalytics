import time
import Chatalytics as c

execution_start_time = time.process_time_ns()

data = c.loadData("private_test_data1.txt")

print(str(data) + "\n\n")

n = 2088

print(f"Index: {n}")
print("Absender: " + str(data.loc[n]["sender"]))
print("Inhalt: " + str(data.loc[n]["message"]))
print("Datum: " + str(data.loc[n]["timestamp"]))