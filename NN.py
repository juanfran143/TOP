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

# Lo único que sirve de momento son las 2 lineas siguientes:
# Nos indican el comportamiento en cada una de las posibilidades
df = pd.read_table("data.txt", sep=";", header=None)

df2 = df.loc[df[4] != 0, [0,1,2,3,4]]
df2 = df2.groupby([0,1,2,3]).mean().reset_index()

df3 = df.loc[df[5] != 0, [0,1,2,3,5]]
df3 = df3.groupby([0,1,2,3]).mean().reset_index()

df4 = df.loc[df[6] != 0, [0,1,2,3,6]]
df4 = df4.groupby([0,1,2,3]).mean().reset_index()

df5 = df.loc[df[7] != 0, [0,1,2,3,7]]
df5 = df5.groupby([0,1,2,3]).mean().reset_index()

a = pd.merge(df2,df3,on=[0,1,2,3],how='outer')
a = pd.merge(a,df4,on=[0,1,2,3],how='outer')
a = pd.merge(a,df5,on=[0,1,2,3],how='outer')
a = a.fillna(0)

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


