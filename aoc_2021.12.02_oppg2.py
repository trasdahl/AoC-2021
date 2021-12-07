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

datafile = "Data/02_input.txt"

df = pd.read_csv(datafile, header=None, sep=' ', names=['direction', 'distance'])
print("Antall tall lest inn   :", df.shape[0])
print(df.head())
print("\n")

# df = df.head()

df['f'] = np.where(df.direction == 'forward', df.distance, 0)
df['d'] = np.where(df.direction == 'down', df.distance, 0)
df['u'] = np.where(df.direction == 'up', df.distance, 0)
df['aim'] = (df.d - df.u).cumsum()
df['forward'] = df.f.cumsum()
df['depth'] = (df.f * df.aim).cumsum()
print(df.head(10))

print("Forward :", df.forward.iloc[-1])
print("Depth   :", df.depth.iloc[-1])

print("Solution:", df.forward.iloc[-1] * df.depth.iloc[-1])



