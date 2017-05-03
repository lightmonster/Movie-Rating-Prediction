import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from dt import ID3Classifier
from lr import MLR
from regressionCalculation import regression
from sklearn import tree
import sklearn.naive_bayes as nb

np.random.seed(0)

#Read data
print("Read data\n")
df_user = pd.read_csv('user.csv')
df_movie = pd.read_csv('movie.csv')
df_train = pd.read_csv('train.csv')
df_test = pd.read_csv('test.csv')
piv_train = df_train.shape[0]#get the dimension
labels = df_train['rating'].values#the attr that we want to predict
df_train = df_train.drop(['rating'],axis=1)


#Preprocessing

##Add test data
frames = [df_train, df_test]
df_train = pd.concat(frames)
# print df_train
##Collect some useful information
uid_test = df_test['user-Id']#df type
mid_test = df_test['movie-Id']#df type
id_test = df_test['Id']

##Modify column label for joining
new_columns = df_user.columns.values
new_columns[0] = 'user-Id'
df_user.columns = new_columns
new_columns = df_movie.columns.values
new_columns[0] = 'movie-Id'
df_movie.columns = new_columns
##Joining
df_train = pd.merge(df_train, df_user, on='user-Id', how='left')
df_train = pd.merge(df_train, df_movie, on='movie-Id', how='left')
# print(df_train)

# print uid_test
# print mid_test
# print labels
dim_train = df_train.shape#dimension of the df: (802762, 9)
# print dim_train
##Drop useless attr
df_train = df_train.drop(['Id'], axis=1)

df_train['Gender'] = df_train['Gender'].replace(np.nan, 'M')
df_train['Age'] = df_train['Age'].fillna(df_train['Age'].mean())
df_train['Occupation'] = df_train['Occupation'].fillna(df_train['Occupation'].mean())
df_train['Year'] = df_train['Year'].fillna(df_train['Year'].mean())

##Fill NaN (except for Gender and Genre)
columns = df_train.columns.values[:-1]
# columns = np.delete(columns, 3)
df_train[columns] = df_train[columns].fillna(-1)
##Handle invalid(wierd) age data
age = df_train.Age.values
# age
# df_train['Age'] = np.where(np.logical_or(age<15), -1, age)
# df_train['Age'] = np.where(np.logical_and(age<25, age>=15), 0, age)
# df_train['Age'] = np.where(np.logical_and(age<35, age>=25), 1, age)
# df_train['Age'] = np.where(np.logical_and(age<45, age>=35), 2, age)
# df_train['Age'] = np.where(age>=45, 3, age)
# year
year = df_train.Year.values
df_train['Year'] = np.where(year<1930, 0, year)
df_train['Year'] = np.where(np.logical_and(year>=1930, year<1940), 1, year)
df_train['Year'] = np.where(np.logical_and(year>=1940, year<1950), 2, year)
df_train['Year'] = np.where(np.logical_and(year>=1950, year<1960), 3, year)
df_train['Year'] = np.where(np.logical_and(year>=1960, year<1970), 4, year)
df_train['Year'] = np.where(np.logical_and(year>=1970, year<1980), 5, year)
df_train['Year'] = np.where(np.logical_and(year>=1980, year<1990), 6, year)
df_train['Year'] = np.where(year>=1990, 7, year)

##Switch columns for better understanding
df_train = df_train[['user-Id','movie-Id','Age','Year','Gender','Occupation','Genre']]
# print df_train
# print pd.cut(df_train['Year'],8,retbins=True)


#Mining data
##One-hot-encoding
# ohe_element = ['Gender','Occupation','Genre','rating']
# ohe_element = ['Gender','Occupation','Age','Year']
# # print df_train.shape
# for e in ohe_element:
#     dummy_table = pd.get_dummies(df_train[e],prefix = e)
#     df_train = df_train.drop([e], axis=1)
#     df_train = pd.concat((df_train, dummy_table), axis=1)
#     # print df_train.shape
#
# ##Reduce dimension of Genre
# genre_list = []
# for genre in df_movie['Genre'].values:
#     if type(genre)==str:
#         genre = genre.split("|")
#         for g in genre:
#             if g not in genre_list:
#                 genre_list.append(g)
# # print genre_list
# genre_dict = dict()
# for i in range(len(genre_list)):
#     genre_dict[genre_list[i]] = i
# # print genre_dict
# genre_table = np.zeros((df_train.shape[0],len(genre_list)))
# # print genre_table.shape # (1000209, 18)
#
# movie_value = df_train['Genre'].values #the attr that we want to predict
# # print movie_value.shape # (1000209,)
#
# for i in range(len(movie_value)):
#     if type(movie_value[i])==str:
#         genre = movie_value[i].split("|")
#         for g in genre:
#             genre_table[i][genre_dict[g]] = 1
# # print genre_table
#
# # print df_train.shape
#
# df_train = df_train.drop(['Genre'], axis=1)
# df_train = pd.concat((df_train, pd.DataFrame(genre_table)), axis=1)
# print df_train

# Mining data
#One-hot-encoding
ohe_element = ['Gender','Occupation','Genre','Age','Year']
# ohe_element = ['Gender','Occupation','rating']
for e in ohe_element:
    dummy_table = pd.get_dummies(df_train[e],prefix = e)
    df_train = df_train.drop([e], axis=1)
    df_train = pd.concat((df_train, dummy_table), axis=1)

#Drop first two columns for predicting
df_train.drop(['user-Id','movie-Id'],axis=1)
# df_train.drop(['Genre'],axis=1)


##Output for debugging
# test = pd.DataFrame(df_train)
# test.to_csv('df_train.csv', index=False)


#Alg
v = df_train.values
X = v[:piv_train]
X_test = v[piv_train:]
# print X
LE = LabelEncoder()
Y = LE.fit_transform(labels)
# print Y

print "MLR"
# model = MLR()
model = nb.BernoulliNB()#Highest score
# model = RandomForestClassifier(n_estimators=500,min_samples_split=200)
# model = tree.DecisionTreeClassifier()
print "fit"
model.fit(X, Y)
print "predict"
predict_prob = model.predict_proba(X_test)


print (predict_prob)

ids, cts = [], []
for i in range(len(id_test)):
    idx = id_test[i]
    ids += [idx]
    cts += LE.inverse_transform(np.argsort(predict_prob[i])[::-1])[:1].tolist()

# generate submission file
sub = pd.DataFrame(np.column_stack((ids, cts)),columns=['id', 'rating'])
sub.to_csv('sub.csv',index=False)
