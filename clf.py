import os
import json
import shutil
import numpy as np

from xgboost import XGBClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import classification_report, confusion_matrix

from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.svm import SVC  # Import the SVC class
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV

from config import WEBSITE_NUM, ACCESS_NUM, ETH_NAME, make_data_set

if not os.path.exists('data'):
    os.mkdir('data')
    shutil.copy('website.txt', 'data/website.txt')

data_set_dir= 'data/dataset_%dC_%dA-%s' % (WEBSITE_NUM, ACCESS_NUM, ETH_NAME)
logs_dir = 'logs_%dC_%dA-%s' % (WEBSITE_NUM, ACCESS_NUM, ETH_NAME)


if not os.path.exists(data_set_dir):
    os.mkdir(data_set_dir)
    make_data_set(logs_dir, data_set_dir)


data_path = 'data/dataset_%dC_%dA-%s/data.npy' % (WEBSITE_NUM, ACCESS_NUM, ETH_NAME)
label_path = 'data/dataset_%dC_%dA-%s/label.npy' % (WEBSITE_NUM, ACCESS_NUM, ETH_NAME)
id_to_name_path = 'data/dataset_%dC_%dA-%s/label_dict.json' % (WEBSITE_NUM, ACCESS_NUM, ETH_NAME)

# X = np.load('data/dataset_10C_100A-enxac15a29872ac/data.npy')
# y = np.load('data/dataset_10C_100A-enxac15a29872ac/label.npy')
# 'data/dataset_10C_100A-enxac15a29872ac/label_dict.json'

X = np.load(data_path)
y = np.load(label_path)

# flatten X to 2D 
# X = X.reshape(X.shape[0], -1)
# extract first 3 columns of the last dimensen and flatten it
# X = X[:, :, :3].reshape(X.shape[0], -1)
# X = X[:, :, :5].reshape(X.shape[0], -1)

X_dim = X.shape[0]
# X = X[:, :, :5] #.reshape(X.shape[0], -1)
col1 = X[:, :, 0].reshape(X_dim, -1)
col2 = X[:, :, 1].reshape(X_dim, -1)
col3 = X[:, :, 2].reshape(X_dim, -1)
col4 = X[:, :, 3].reshape(X_dim, -1)
col5 = X[:, :, 4].reshape(X_dim, -1)
col6 = X[:, :, 5].reshape(X_dim, -1)
col7 = X[:, :, 6].reshape(X_dim, -1)

X = np.concatenate((col2, ), axis=1) #, col2, col3, col4, col5, col6, col7

# X = X[:, 300:]

id_to_name: dict = json.load(open(id_to_name_path, 'rb'))

target_names = [id_to_name[i] for i in sorted(id_to_name.keys())]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

scaler = StandardScaler()
scaler.fit(X_train)

X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)

print(X_train.shape, X_test.shape, y_train.shape, y_test.shape)

# models = []
# model = XGBClassifier(nthread=os.cpu_count() // 2)
# model = RandomForestClassifier(n_jobs=os.cpu_count() // 2)
# model = DecisionTreeClassifier()
# model = SVC(kernel='linear', probability=True)
model = MLPClassifier(max_iter=1000, random_state=42, hidden_layer_sizes=(200,100))
# model = SVC(kernel='linear', probability=True)
# modle = SVC(kernel='linear', C=1, probability=True, nthread=os.cpu_count() // 2)
# model = SVC(kernel='linear')

mlp = MLPClassifier(max_iter=500, random_state=80) 
pipeline = Pipeline([ ('scaler', scaler), ('mlp', mlp) ])
param_grid = {'mlp__hidden_layer_sizes': [(200,200), (200, 200, 100), (400,)], 
            # 'mlp__activation': ['relu', 'tanh'], 
            # 'mlp__solver': ['adam', 'sgd'], 
            # 'mlp__alpha': [0.0001, 0.001, 0.01], 
            # 'mlp__learning_rate': ['constant', 'adaptive'] 
            }
# model = GridSearchCV(pipeline, param_grid, cv=5, n_jobs=-1)
# grid_search.fit(X, y)
# model = mlp
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
# print(model.cv_results_)

print(classification_report(y_test, y_pred, target_names=target_names, digits=4))
print(cross_val_score(model, X, y, cv=5, scoring='accuracy'))
# print(y_train)
# print(y_pred)
# print(y_test)
