"""
The first order of business is to figure out how quickly the depth increases, just so you know what you're dealing with - you never know if the keys will get carried into deeper water by an ocean current or a fish or something.

To do this, count the number of times a depth measurement increases from the previous measurement. (There is no measurement before the first measurement.) In the example above, the changes are as follows:

199 (N/A - no previous measurement)
200 (increased)
208 (increased)
210 (increased)
200 (decreased)
207 (increased)
240 (increased)
269 (increased)
260 (decreased)
263 (increased)
In this example, there are 7 measurements that are larger than the previous measurement.
"""

import numpy as np
import pandas as pd
import os

datafile = "Data/01_input.txt"
df = pd.read_csv(datafile, header=None)
print("Antall tall lest inn   :", df.shape[0])
a = df.values

print("Antall som øker, pandas:", ((df - df.shift()) > 0).sum().values[0])

print("Antall som øker, numpy :", ((a[1:] - a[:-1]) > 0).sum())
