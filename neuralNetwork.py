import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
import keras
from keras import layers

data = pd.read_csv("test.csv")

data['Label'] = np.where(data['124'].shift(-1) > data['124'], 1, 0)

features = [str(i) for i in range(125)]
X = data[features].values
y = data['Label'].values

X_train, X_test, y_train, y_test = train_test_split(X,y, test_size=0.2, random_state=42)

scaler = MinMaxScaler()

X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

model = keras.Sequential()
model.add(layers.LSTM(50, input_shape=(X_train.shape[1], 1)))
model.add(layers.Dense(1, activation='sigmoid'))
model.compile(optimizer='adam',loss='binary_crossentropy', metrics =['accuracy'])

X_train = X_train.reshape((X_train.shape[0], X_train.shape[1], 1))
X_test = X_test.reshape((X_test.shape[0], X_test.shape[1], 1))
print(X_train)
model.fit(X_train, y_train, epochs=10, batch_size=32, validation_split=0.1)

loss, accuracy = model.evaluate(X_test,y_test)
print(f'Test Accuracy: {accuracy}')