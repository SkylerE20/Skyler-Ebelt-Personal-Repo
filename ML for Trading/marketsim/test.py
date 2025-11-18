import pandas as pd
import numpy as np
test = pd.DataFrame(np.random.randint(0,5, 5))
#print(test)
data = pd.DataFrame(np.zeros(shape = (5,2)))
for i in range(data.shape[0]):
    for j in range(data.shape[1]):
        data.iloc[i,j] = test.iloc[i]

#print(data.loc[:,0])

syms = ['a', 'b', 'c', 'd']
print(syms)
syms.append('e')
syms.append('f')
print(syms)

allocs_per_date = pd.DataFrame(np.zeros((10, 4 + 2)))
allocs_per_date.columns = [syms]
#print(allocs_per_date)
allocs_per_date.index = ('t1','t2','t3','t4', 't5', 't6', 't7', 't8', 't9', 't10')
print(allocs_per_date)
print(allocs_per_date.iloc[:,0:-2])
test = allocs_per_date.iloc[:,0:-2]
allocs_per_date.iloc[0,0] = 2
allocs_per_date.iloc[1,0] = 1
allocs_per_date.iloc[0,0] = allocs_per_date.iloc[0,0] - allocs_per_date.iloc[1,0]
print(allocs_per_date)
print(allocs_per_date.shape[0])
print(allocs_per_date.shape[1])

for n in range(allocs_per_date.iloc[:,0:-1].shape[0]):
    if n == 0:
        print(allocs_per_date.index[n])
    if n != 0 and n > 1:
        print(allocs_per_date.index[n-1])

#for i in test.shape[1]:
#    print(allocs_per_date.index[i])

print("test",allocs_per_date.index[0])

for i in range(10):
    for j in range(6):
        allocs_per_date.iloc[i,j] = int(j) + int(i)

for i in range(10):
    for j in range(6):
        allocs_per_date.iloc[i,j] = allocs_per_date.iloc[i - 1 ,j] + 100
print(allocs_per_date)


n = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']

for i in n:
    print(i)
test = allocs_per_date.shape[1]

allocs_per_date.iloc[2,0:-3] = allocs_per_date.iloc[3,0:-3]
print(allocs_per_date)

import datetime as dt

hdates = [dt.datetime(2007, 1, 15), dt.datetime(2007, 2, 19), dt.datetime(2007, 4, 6),
              dt.datetime(2007, 5, 28), dt.datetime(2007, 7, 4),
              dt.datetime(2007, 9, 3), dt.datetime(2007, 11, 22), dt.datetime(2007, 12, 25),
              dt.datetime(2008, 1, 21), dt.datetime(2008, 2, 18), dt.datetime(2007, 3, 21),
              dt.datetime(2008, 5, 26), dt.datetime(2008, 7, 4),
              dt.datetime(2008, 9, 1), dt.datetime(2007, 11, 27), dt.datetime(2008, 12, 25),
              dt.datetime(2009, 1, 19), dt.datetime(2009, 2, 16), dt.datetime(2009, 4, 10),
              dt.datetime(2009, 5, 25), dt.datetime(2009, 7, 3),
              dt.datetime(2009, 9, 7), dt.datetime(2009, 11, 26), dt.datetime(2009, 12, 25),
              dt.datetime(2010, 1, 18), dt.datetime(2010, 2, 15), dt.datetime(2010, 4, 2),
              dt.datetime(2010, 5, 31), dt.datetime(2010, 7, 5),
              dt.datetime(2010, 9, 6), dt.datetime(2010, 11, 25), dt.datetime(2010, 12, 24),
              dt.datetime(2011, 1, 17), dt.datetime(2011, 2, 21), dt.datetime(2011, 4, 22),
              dt.datetime(2011, 5, 30), dt.datetime(2011, 7, 4),
              dt.datetime(2011, 9, 5), dt.datetime(2011, 11, 24), dt.datetime(2011, 12, 26),
              dt.datetime(2012, 1, 16), dt.datetime(2012, 2, 20), dt.datetime(2012, 4, 6),
              dt.datetime(2012, 5, 28), dt.datetime(2012, 7, 4),
              dt.datetime(2012, 9, 3), dt.datetime(2012, 11, 22), dt.datetime(2012, 12, 25)
              ]

index_rm = ['t1', 't5']

"""for i in index_rm:
    for j in range(allocs_per_date.shape[0]):
        if allocs_per_date.index[j] == i:
            allocs_per_date.drop[j]
        else:
            pass"""
allocs_per_date.drop(index = index_rm, inplace = True)

print(allocs_per_date)

index = pd.date_range(start = dt.datetime(2007, 1, 15), end = dt.datetime(2007, 2, 19))
todrop = [dt.datetime(2007, 1, 15), dt.datetime(2007, 2, 19)]
index = index.drop(todrop)
print(index)

if all(allocs_per_date.iloc[2,0:-1]) == all(allocs_per_date.iloc[1,0:-1]):
    print("all done")

print(allocs_per_date.index[2])