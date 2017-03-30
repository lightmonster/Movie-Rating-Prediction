import math
import numpy as np
import sys

#Variables declared here
filename = sys.argv[1]
GYlist = []
user_dict = dict()

#Object defined here
class RateInfo:
    def __init__(self, movie, rating):
        self.movie = movie
        self.rating = rating


#Function defined here



#init GYlist
for i in range(18):
    #slots of genre
    temp = []
    for j in range(8):
        #slots of year
        temp.append(None)
    GYlist.append(temp)
print GYlist[2][3]

#read from file
with open(filename) as f:
    data = f.readlines()

for n, line in enumerate(data, 1):
    cur_entry = line.rstrip().split(',')
    # print line.rstrip().split(',')
    #[ id     , user_id, movie_id, rate]
    #['160931', '504'  , '3934'  , '4' ]
    if (cur_entry[1] not in user_dict):
        user_dict[cur_entry[1]] = [RateInfo(cur_entry[2], cur_entry[3])]
    else:
        user_dict[cur_entry[1]].append(RateInfo(cur_entry[2], cur_entry[3]))

for row in user_dict.values():
    for ele in row:
        print ele.movie
