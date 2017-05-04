import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.neighbors import KNeighborsClassifier
#from nbc import NaiveBayesClassifier
from dt import ID3Classifier
from lr import MLR

#TODO:
    # Integrate all data set together and form a DataFrame: df_train, df_test
    #

print("test==w==")

np.random.seed(0)

#Loading data
df_train = pd.read_csv('train_users_2.csv')
df_test = pd.read_csv('test_users.csv')
labels = df_train['country_destination'].values
df_train = df_train.drop(['country_destination'], axis=1)
id_test = df_test['id']
piv_train = df_train.shape[0]#get the dimension

print(df_train)
# print(piv_train)
print(df_train.shape)

#Creating a DataFrame with train+test data
df_all = pd.concat((df_train, df_test), axis=0, ignore_index=True)
#Removing id and date_first_booking
df_all = df_all.drop(['id', 'date_first_booking'], axis=1)
#Filling nan
df_all = df_all.fillna(-1)

print(df_all)#integration

#####Feature engineering#######
#date_account_created
dac = np.vstack(df_all.date_account_created.astype(str).apply(lambda x: list(map(int, x.split('-')))).values)

print("dac: {}").format(dac)#Seprate the date into 2D vertical array [[2010    6   28] [2011    5   25]]

df_all['dac_year'] = dac[:,0]
df_all['dac_month'] = dac[:,1]
df_all['dac_day'] = dac[:,2]
df_all = df_all.drop(['date_account_created'], axis=1)


#timestamp_first_active
tfa = np.vstack(df_all.timestamp_first_active.astype(str).apply(lambda x: list(map(int, [x[:4],x[4:6],x[6:8],x[8:10],x[10:12],x[12:14]]))).values)
df_all['tfa_year'] = tfa[:,0]
df_all['tfa_month'] = tfa[:,1]
df_all['tfa_day'] = tfa[:,2]
df_all = df_all.drop(['timestamp_first_active'], axis=1)

print("tfa:{}").format(tfa)

#Age
av = df_all.age.values
df_all['age'] = np.where(np.logical_or(av<14, av>100), -1, av)#prune age data that <14 or >100

print("age")
print(df_all['age'])

#One-hot-encoding features
ohe_feats = ['gender', 'signup_method', 'signup_flow', 'language', 'affiliate_channel', 'affiliate_provider', 'first_affiliate_tracked', 'signup_app', 'first_device_type', 'first_browser']
for f in ohe_feats:
    df_all_dummy = pd.get_dummies(df_all[f], prefix=f)#Convert categorical variable into dummy/indicator variables
    df_all = df_all.drop([f], axis=1)
    df_all = pd.concat((df_all, df_all_dummy), axis=1)

# print(df_all)
#using One-hot-encoding method to generate table for each of the attribuate

#test. export df_all to csv
test = pd.DataFrame(df_all)
test.to_csv('check.csv', index=False)

#Splitting train and test
vals = df_all.values
print ("========w=========")
print (vals)
X = vals[:piv_train]
le = LabelEncoder()#Encode labels with value between 0 and n_classes-1.
y = le.fit_transform(labels)#Fit label encoder and return encoded labels
# print(y)
X_test = vals[piv_train:]

model = MLR()
model.fit(X, y)
predict_prob = model.predict_proba(X_test)

print (predict_prob)


# take the 5 highest probabilities class
ids, cts = [], []
for i in range(len(id_test)):
    idx = id_test[i]
    ids += [idx]*5
    cts += le.inverse_transform(np.argsort(predict_prob[i])[::-1])[:5].tolist()

#for i in range(len(ids)):
#	print ids

#for i in range(len(cts)):
#	print (i)

# generate submission file
# sub = pd.DataFrame(np.column_stack((ids, cts)),columns=['id', 'country'])
# sub.to_csv('sub.csv',index=False)