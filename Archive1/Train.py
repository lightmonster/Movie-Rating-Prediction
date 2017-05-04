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
genre_dict = dict()

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

#init genre_dict
genre_dict["Action"] = 0
genre_dict["Adventure"] = 1
genre_dict["Animation"] = 2
genre_dict["Children's"] = 3
genre_dict["Comedy"] = 4
genre_dict["Crime"] = 5
genre_dict["Documentary"] = 6
genre_dict["Drama"] = 7
genre_dict["Fantasy"] = 8
genre_dict["Film-Noir"] = 9
genre_dict["Horror"] = 10
genre_dict["Mystery"] = 11
genre_dict["Musical"] = 12
genre_dict["Romance"] = 13
genre_dict["Sci-Fi"] = 14
genre_dict["Thriller"] = 15
genre_dict["War"] = 16
genre_dict["Western"] = 17
genre_dict[None] = 18

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
    #decide location
    #for none data
    if (cur_movie_y == None):
        gy_y = 8
    else:
        gy_y = min_max(year_start, year_end, cur_movie_y)

    if (cur_movie_g == None):
        gy_x = 18
        #Assign tuple to location
        GYlist[gy_x][gy_y].append(cur_tuple)
    else:
        for g in cur_movie_g:
            gy_x = genre_dict[g]
            #Assign tuple to location
            GYlist[gy_x][gy_y].append(cur_tuple)

#testing
print GYlist[0][0]

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
