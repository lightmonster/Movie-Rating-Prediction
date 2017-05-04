import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import sklearn.naive_bayes as nb
from sklearn.ensemble import RandomForestClassifier
from sklearn import svm
from sklearn.neighbors import KNeighborsClassifier

np.random.seed(0)
# Loading data
df_train = pd.read_csv('train_users_2.csv')
df_test = pd.read_csv('test_users.csv')
labels = df_train['country_destination'].values
df_train = df_train.drop(['country_destination'], axis=1)
id_test = df_test['id']

# Creating a DataFrame with train data
# Removing id and date_first_booking
df_train = df_train.drop(['id', 'date_first_booking'], axis=1)
# Filling nan
df_train = df_train.fillna(-1)


# date_account_created
dac = np.vstack(df_train.date_account_created.astype(str).apply(lambda x: list(map(int, x.split('-')))).values)
df_train['dac_year'] = dac[:,0]
df_train['dac_month'] = dac[:,1]
df_train['dac_day'] = dac[:,2]
df_train = df_train.drop(['date_account_created'], axis=1)

# timestamp_first_active
tfa = np.vstack(df_train.timestamp_first_active.astype(str).apply(lambda x: list(map(int, [x[:4],x[4:6],x[6:8],x[8:10],x[10:12],x[12:14]]))).values)
df_train['tfa_year'] = tfa[:,0]
df_train['tfa_month'] = tfa[:,1]
df_train['tfa_day'] = tfa[:,2]
df_train = df_train.drop(['timestamp_first_active'], axis=1)

# Age
av = df_train.age.values
df_train['age'] = np.where(np.logical_or(av<14, av>100), -1, av)

features = ['gender', 'signup_method', 'signup_flow', 'language', 'affiliate_channel', 'affiliate_provider', 'first_affiliate_tracked', 'signup_app', 'first_device_type', 'first_browser']
for f in features:
    df_train[f] = pd.Categorical.from_array(df_train[f]).codes

x = df_train.values
le = LabelEncoder()
y = le.fit_transform(labels)

# Classifier
# model = nb.BernoulliNB()
# model.fit(x, y)
# predict_prob = model.predict_proba(x)

# model = svm.SVC()
# model.fit(x, y)
# predict_prob = model.predict_proba(x)

# model = KNeighborsClassifier(n_neighbors=10)
# model.fit(x, y)
# predict_prob = model.predict_proba(x)

model = RandomForestClassifier(n_estimators=500,min_samples_split=200)
model.fit(x, y)
predict_prob = model.predict_proba(x)

#Taking the 5 classes with highest probabilities
ids = []  #list of ids
cts = []  #list of countries
for i in range(len(id_test)):
    idx = id_test[i]
    ids += [idx] * 5
    cts += le.inverse_transform(np.argsort(predict_prob[i])[::-1])[:5].tolist()

#Generate submission
sub = pd.DataFrame(np.column_stack((ids, cts)), columns=['id', 'country'])
sub.to_csv('sub.csv',index=False)
