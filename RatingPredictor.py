from __future__ import print_function
from __future__ import division
import numpy as np
import pandas as pd
import nb_manual as nb

# Read data from txt files
print ("Read data")
df_user = pd.read_csv('user.txt')
df_movie = pd.read_csv('movie.txt')
df_train = pd.read_csv('train.txt')
df_test = pd.read_csv('test.txt')
piv_train = df_train.shape[0]  # get the number of training
labels = df_train['rating'].values  # the rating that we want to predict
id_test = df_test['Id']

# Preprocessing

# Merging
df_train = df_train.drop(['rating'], axis=1)  # we don't need rating
frames = [df_train, df_test]
df_train = pd.concat(frames)  # merge

# Modify column label for joining
new_columns = df_user.columns.values
new_columns[0] = 'user-Id'
df_user.columns = new_columns
new_columns = df_movie.columns.values
new_columns[0] = 'movie-Id'
df_movie.columns = new_columns
# Joining
df_train = pd.merge(df_train, df_user, on='user-Id', how='left')
df_train = pd.merge(df_train, df_movie, on='movie-Id', how='left')

df_train = df_train.drop(['Id'], axis=1)

# Fill NaN (except for Gender and Genre)
columns = df_train.columns.values[:-1]
df_train[columns] = df_train[columns].fillna(-1)  # missing data

# Switch columns for better understanding
df_train = df_train[['user-Id', 'movie-Id', 'Age', 'Year', 'Gender', 'Occupation', 'Genre']]

# Mining data: One-hot-encoding
ohe_element = ['Gender', 'Occupation', 'Genre', 'Age', 'Year']
for e in ohe_element:
    dummy_table = pd.get_dummies(df_train[e], prefix=e)
    df_train = df_train.drop([e], axis=1)
    df_train = pd.concat((df_train, dummy_table), axis=1)

# genre_list = []
# for genre in df_movie['Genre'].values:
#     if type(genre) == str:
#         genre = genre.split("|")
#         for g in genre:
#             if g not in genre_list:
#                 genre_list.append(g)
# genre_dict = dict()
# for i in range(len(genre_list)):
#     genre_dict[genre_list[i]] = i
# genre_table = np.zeros((df_train.shape[0], len(genre_list)))
# movie_value = df_train['Genre'].values  # the attr that we want to predict
# for i in range(len(movie_value)):
#     if type(movie_value[i]) == str:
#         genre = movie_value[i].split("|")
#         for g in genre:
#             genre_table[i][genre_dict[g]] = 1
#
# df_train = df_train.drop(['Genre'], axis=1)
# df_train = pd.concat((df_train, pd.DataFrame(genre_table)), axis=1)

# Drop first two columns for predicting
df_train.drop(['user-Id', 'movie-Id'], axis=1)

# Output for debugging
# test = pd.DataFrame(df_train)
# test.to_csv('df_train.csv', index=False)

# Algorithm
v = df_train.values
X = v[:piv_train]
X_test = v[piv_train:]

print ("BernoulliNB")
model = nb.BernoulliNB()  # Highest score
print ("fit")
model.fit(X, labels)
print ("predict")
predict_prob = model.predict_log_proba(X_test)

ids, cts, cts1 = [], [], []
for i in range(len(id_test)):
    idx = id_test[i]
    ids += [idx]
    cts += (np.argsort(predict_prob[i])[::-1] + 1)[:1].tolist()
# print (cts)

# generate submission file
sub = pd.DataFrame(np.column_stack((ids, cts)), columns=['id', 'rating'])
sub.to_csv('sub_ylabel.csv', index=False)
