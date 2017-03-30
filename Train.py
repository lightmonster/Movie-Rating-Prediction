import math
import numpy as np
import sys
from collections import Counter


#Variables declared here
filename = sys.argv[1]
GYlist = []
year_start = 1919
year_end = 2000
user_dict = dict()

#for read movie
num_movie = -1
dict_movie = {} # id: Movie(year,genre)
genre_counter = Counter()
year_max = 0
year_min = 2000

#Object defined here
class Movie:
    def __init__(self,year, genre):
        self.year = year
        self.genre = genre



#Function defined here
def min_max (min_a, max_a, v):
    return 7*(v-min_a)/(max_a-min_a)


#init GYlist
for i in range(19):
    #slots of genre
    temp = []
    for j in range(9):
        #slots of year
        temp.append([])
    GYlist.append(temp)
print GYlist[2][3]

#read movie from file
read_movie = open("movie.txt", "r")
for line in read_movie:
    if num_movie != -1:
        words = line.split(',')
        # words[1]: year
        if words[1] == 'N/A':
            words[1] = None
        else:
            words[1] = int(words[1])
            year_max = max(year_max,words[1])
            year_min = min(year_min,words[1])
        # words[2]: genre
        words[2] = words[2].strip()
        if words[2] == 'N/A':
            words[2] = None
        else:
            words[2] = words[2].split('|')
            for g in words[2]:
                genre_counter[g] += 1
        dict_movie[words[0]] = Movie(words[1],words[2])
    num_movie += 1
#access by read dict_movie

#read train from file
with open(filename) as f:
    data = f.readlines()

for n, line in enumerate(data, 1):
    cur_entry = line.rstrip().split(',')
    #handle first line which is useless
    if (cur_entry[0] == "Id"): continue
    #[ id     , user_id, movie_id, rate]
    #['160931', '504'  , '3934'  , '4' ]
    cur_tuple = (cur_entry[1], cur_entry[3])
    # print cur_entry[2]
    cur_movie_g = dict_movie[cur_entry[2]].genre
    cur_movie_y = dict_movie[cur_entry[2]].year
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
    elif (cur_movie_g == "None"):
        gy_x = 17
    else:
        gy_x = 18
    #for none data
    if (cur_movie_y == None):
        gy_y = 8
    else:
        gy_y = min_max(year_start, year_end, cur_movie_y)
    #Assign tuple to location
    GYlist[gy_x][gy_y].append(cur_tuple)

print GYlist

# for row in user_dict.values():
#     for ele in row:
#         print ele.movie


#Recycle bin

# print line.rstrip().split(',')

# if (cur_entry[1] not in user_dict):
#     user_dict[cur_entry[1]] = [RateInfo(cur_entry[2], cur_entry[3])]
# else:
#     user_dict[cur_entry[1]].append(RateInfo(cur_entry[2], cur_entry[3]))

# class RateInfo:
#     def __init__(self, movie, rating):
#         self.movie = movie
#         self.rating = rating
