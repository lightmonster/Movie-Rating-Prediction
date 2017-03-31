import math
import numpy as np
import sys
from collections import Counter

# Variables: User

user_dictionary = dict()
lines = []
count_user = -1

# Variables: Movie

num_movie = -1
num_genre = 0
dict_movie = {} # id: Movie(year,genre)
genre_counter = Counter()
year_max = 0
year_min = 2000

# Variables: Train

genre_dict = dict()
GYlist = []
model = []

# Object: User

class User:
    def __init__(self,ID,gender,age,occupation):
        self.ID = ID
        if gender != "N/A":
            if gender == 'M':
                self.gender = 0
            else:
                self.gender = 1
        else:
            self.gender = None
        if age != "N/A":
            self.age = age
        else:
            self.age = None
        if occupation != "N/A":
            self.occupation = occupation
        else:
            self.occupation = None

# Object: Movie

class Movie:
    def __init__(self, year, genre):
        self.year = year
        self.genre = genre

# Functions defined here

def min_max (min_a, max_a, v):
    return 7*(v-min_a)/(max_a-min_a)

# Debug
def print_dict_u (d):
    key_list = sorted(d.keys())
    for k in key_list:
        print k, d[k].gender, d[k].age, d[k].occupation
def print_dict_m (d):
    key_list = sorted(d.keys())
    for k in key_list:
        print k, d[k].year, d[k].genre

def regression (X, y): # return b_list, mean of err_list
    n = len(X)
    # (1) X'y Matrix
    Xt = np.transpose (X)
    X_y = np.dot (Xt, y)
    # (2) X'X Matrix
    Xt_X = np.dot (Xt, X)
    # (6) Inverse Matrix
    inv_Xt_X = np.linalg.inv(Xt_X)
    b_list = np.dot(inv_Xt_X, X_y)
    err_list = []
    for i in range(n):
        err_list.append(y[i] - np.dot (b_list,X[i]))
    return [b_list, np.mean(err_list)]

# Extract Data: User

file_ = open("user.txt", "r")

for line in file_:
    lines.append(line)
    count_user += 1

file_.close()

for i in range(1,count_user + 1):
    result = (lines[i].strip()).split(",")
    temp_user = User(result[0],result[1],result[2],result[3])
    user_dictionary[result[0]] = temp_user

# print_dict_u (user_dictionary)

# Extract Data: Movie

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

read_movie.close()

# print_dict_m (dict_movie)

# Train

# init genre_dict
for genre in sorted(genre_counter.keys()):
	genre_dict[genre] = num_genre
	num_genre += 1
genre_dict[None] = i

# init GYlist & model
for i in range(num_genre+1):
    # slots of genre
    temp = []
    for j in range(9):
        # slots of year
        temp.append([])
    GYlist.append(temp)
    model.append(temp) # model[i][j] = [b_double_array, err_array]

# Extract Data: Train

with open("train.txt") as f:
    data = f.readlines()

for n, line in enumerate(data, 1):
    cur_entry = line.rstrip().split(',')
    # handle first line which is useless
    if (cur_entry[0] == "Id"): continue
    # [ id     , user_id, movie_id, rate]
    # ['160931', '504'  , '3934'  , '4' ]
    cur_tuple = (cur_entry[1], cur_entry[3])
    cur_movie_g = dict_movie[cur_entry[2]].genre
    cur_movie_y = dict_movie[cur_entry[2]].year
    # decide location
    # for none data
    if (cur_movie_y == None):
        gy_y = 8
    else:
        gy_y = min_max(year_min, year_max, cur_movie_y)
    if (cur_movie_g == None):
        gy_x = num_genre
        # Assign tuple to location
        GYlist[gy_x][gy_y].append(cur_tuple)
    else:
        for g in cur_movie_g:
            gy_x = genre_dict[g]
            # Assign tuple to location
            GYlist[gy_x][gy_y].append(cur_tuple)

for i in range(num_genre+1):
    for j in range(9):
        target_list = GYlist[i][j]
        user_list = []
        rating_list = []
        count_gender = count_age = count_occupation = 0
        sum_gender = sum_age = sum_occupation = 0
        avg_gender = avg_age = avg_occupation = 0
        for target in target_list:
            if user_dictionary[target[0]].gender != None:
                user_dictionary[target[0]].gender = int(user_dictionary[target[0]].gender)
                sum_gender += user_dictionary[target[0]].gender
                count_gender += 1
            if user_dictionary[target[0]].age != None:
                user_dictionary[target[0]].age = int(user_dictionary[target[0]].age)
                sum_age += user_dictionary[target[0]].age
                count_age += 1
            if user_dictionary[target[0]].occupation != None:
                user_dictionary[target[0]].occupation = int(user_dictionary[target[0]].occupation)
                sum_occupation += user_dictionary[target[0]].occupation
                count_occupation += 1
        if count_gender != 0:
            avg_gender = sum_gender*1.0/count_gender
        if count_age != 0:
            avg_age = sum_age*1.0/count_age
        if count_occupation != 0:
            avg_occupation = sum_occupation*1.0/count_occupation
        for target in target_list:
            temp = []
            if user_dictionary[target[0]].gender != None:
                temp.append(float(user_dictionary[target[0]].gender))
            else:
                temp.append(avg_gender)
            if user_dictionary[target[0]].age != None:
                temp.append(float(user_dictionary[target[0]].age))
            else:
                temp.append(avg_age)
            if user_dictionary[target[0]].occupation != None:
                temp.append(float(user_dictionary[target[0]].occupation))
            else:
                temp.append(avg_occupation)
            user_list.append(temp)
            rating_list.append(float(target[1]))
        user_list = np.array(user_list)
        rating_list = np.array(rating_list)
        model[i][j] = regression (user_list, rating_list)
print model

#
# def get_expected_rating(user, movie):
# 	return 1
#
# file_test = open("test.txt","r")
# line_test = []
# for line in file_test:
# 	line_test.append(line)
#
# for i in range(1, len(line_test)):
# 	parse_line = line_test[i].split(",")
# 	rating = get_expected_rating(parse_line[1],parse_line[2])
# 	j = str(parse_line[0]) + " "
# 	j += str(rating)
# 	print(j)
