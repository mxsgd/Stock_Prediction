import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
import keras
from keras import layers

data = pd.read_csv("raw_stock_test.csv")
column_names = data.columns
column_names.drop('return_1m')

#data['Label'] = np.where(data['return_1m'] > 0, 1, 0)
bins = [-np.inf, 0, 0.05, 0.15, np.inf]
labels = [0, 1, 2, 3]
labels = pd.cut(data['return_1m'], bins=bins, labels=False).values
print(labels)
data['Label'] = labels
print(data['Label'])
data = data.dropna()
print(len(data))

data.replace([np.inf, -np.inf], np.finfo(np.float64).max, inplace=True)
X = data[column_names].values
data.to_csv("pre_learning.csv", index=False)
y = keras.utils.to_categorical(data['Label'].values, num_classes=4)

X_train, X_test, y_train, y_test = train_test_split(X,y, test_size=0.2, random_state=48)

scaler = MinMaxScaler()
scaler.fit(X_train)
X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)

model = keras.Sequential()
model.add(layers.LSTM(50, input_shape=(1, len(column_names))))
# model.add(layers.Dropout(0.2))
# model.add(layers.LSTM(50))
# model.add(layers.Dropout(0.2))
# model.add(layers.LSTM(50))
# model.add(layers.Dropout(0.2))
model.add(layers.Dense(4, activation='softmax'))
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

X_train = X_train.reshape((X_train.shape[0], 1, X_train.shape[1]))
X_test = X_test.reshape((X_test.shape[0], 1, X_test.shape[1]))

model.fit(X_train, y_train, epochs=10, batch_size=32, validation_split=0.1)

model.save("lstm_model.h5")
loss, accuracy = model.evaluate(X_test,y_test)
print(f'Test Accuracy: {accuracy}')