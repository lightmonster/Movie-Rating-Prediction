import sys
from collections import Counter

read_movie = open("movie.txt", "r")

class Movie:
    def __init__(self,year, genre):
        self.year = year
        self.genre = genre

num_movie = -1

dict_movie = {} # id: Movie(year,genre)
genre_counter = Counter()
year_max = 0
year_min = 2000

def min_max (min_a, max_a, v):
    print max_a,min_a
    return 7*(v-min_a)/(max_a-min_a)

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

# Debug
def print_dict (d):
    key_list = sorted(d.keys())
    for k in key_list:
        print k, d[k].year, d[k].genre

# print "Movie Count:", num_movie
# print "Year Range: [", year_min, ",", year_max, "]"
# print "Genre List:", sorted(genre_counter.keys())
# print "Genre Count:", len(genre_counter.keys())
# print_dict (dict_movie)
