import math
import numpy as np
import sys

#Variables declared here
filename = sys.argv[1]
GYlist = []
year_start = 1919
year_end = 2000
user_dict = dict()

#Object defined here
class RateInfo:
    def __init__(self, movie, rating):
        self.movie = movie
        self.rating = rating


#Function defined here
def min_max (min_a, max_a, v):
    return 7*(v-min_a)/(max_a-min_a)


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
    #[ id     , user_id, movie_id, rate]
    #['160931', '504'  , '3934'  , '4' ]
    cur_tuple = (cur_entry[1], cur_entry[3])
    cur_movie_g = "Action"#find the movie genre
    cur_movie_y = 1980#find the movie year
    gy_x = -1
    gy_y = -1

    #decide location
    if (cur_movie_g == "Action"):
        gy_x = 0
    elif (cur_movie_g == "Adventure"):
        gy_x = 1
    elif (cur_movie_g == "Animation"):
        gy_x = 2
    elif (cur_movie_g == "Children's"):
        gy_x = 3
    elif (cur_movie_g == "Comedy"):
        gy_x = 4
    elif (cur_movie_g == "Crime"):
        gy_x = 5
    elif (cur_movie_g == "Documentary"):
        gy_x = 6
    elif (cur_movie_g == "Drama"):
        gy_x = 7
    elif (cur_movie_g == "Fantasy"):
        gy_x = 8
    elif (cur_movie_g == "Film-Noir"):
        gy_x = 9
    elif (cur_movie_g == "Horror"):
        gy_x = 10
    elif (cur_movie_g == "Mystery"):
        gy_x = 11
    elif (cur_movie_g == "Musical"):
        gy_x = 12
    elif (cur_movie_g == "Romance"):
        gy_x = 13
    elif (cur_movie_g == "Sci-Fi"):
        gy_x = 14
    elif (cur_movie_g == "Thriller"):
        gy_x = 15
    elif (cur_movie_g == "War"):
        gy_x = 16
    else:
        gy_x = 17
    gy_y = min_max(year_start, year_end, cur_movie_y)
    #Assign tuple to location
    GYlist[gy_x][gy_y] = cur_tuple

# for row in user_dict.values():
#     for ele in row:
#         print ele.movie


#Recycle bin

# print line.rstrip().split(',')

# if (cur_entry[1] not in user_dict):
#     user_dict[cur_entry[1]] = [RateInfo(cur_entry[2], cur_entry[3])]
# else:
#     user_dict[cur_entry[1]].append(RateInfo(cur_entry[2], cur_entry[3]))
