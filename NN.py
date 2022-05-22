import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from keras.wrappers.scikit_learn import KerasClassifier
from keras.utils import np_utils
from classes import node
# for modeling
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.callbacks import EarlyStopping


df = pd.read_table("data.txt", sep=";", header=None)
df = df.groupby([0,1,2,3]).mean().reset_index()

# shuffle the dataset!
#df = df.sample(frac=1).reset_index(drop=True)


nodes = []

nodes.append(node(0, 0, 1, 1))
nodes.append(node(1, 1, 2, 2))
nodes.append(node(2, 2, 1, -1))
nodes.append(node(3, 3, 0, 0))
nodes.append(node(4, 4, 3, 3))
nodes.append(node(5, 0, 4, 4))



Y = df.iloc[:, len(nodes)-1:]
X = df.iloc[:, 0:(len(nodes)-1)]

print(X.shape)
print(Y.shape)

# convert to numpy arrays
X = np.array(X)


model = Sequential()
model.add(Dense(16, input_shape=(X.shape[1],), activation='relu')) # input shape is (features,)
model.add(Dense(Y.shape[1], activation='softmax'))
model.summary()

# compile the model
model.compile(optimizer='rmsprop',
              loss='categorical_crossentropy', # this is different instead of binary_crossentropy (for regular classification)
              metrics=['accuracy'])


