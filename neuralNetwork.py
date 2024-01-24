import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
import keras
from keras import layers
import tensorflow as tf

print("Num GPUs Available: ", len(tf.config.experimental.list_physical_devices('GPU')))
data = pd.read_csv("calculated_stock_test.csv")

data['Label'] = np.where(data['Close'].shift(-1) > data['Close'], 1, 0)

# columns_to_exclude = (
#     list(range(0, data.shape[1], 9)) +
#     list(range(1, data.shape[1], 9)) +
#     list(range(2, data.shape[1], 9)) +
#     list(range(3, data.shape[1], 9))
# )
# valid_columns = [col for col in columns_to_exclude if col < data.shape[1] and col != 603]
# data = data.drop(data.columns[valid_columns], axis=1)

# data = data.drop(data.index[::12]).reset_index(drop=True)
print(len(data))
data = data.dropna()
data.replace([np.inf, -np.inf], np.finfo(np.float64).max, inplace=True)
features_to_exclude = []
# features = [str(i) for i in range(3)]
features = ['Short_MA','Long_MA','MACD','Signal_Line','Above', 'Below','VolumeToPrice']
X = data[features].values
data.to_csv("pre_learning.csv", index=False)
y = data['Label'].values

X_train, X_test, y_train, y_test = train_test_split(X,y, test_size=0.2, random_state=48)

scaler = MinMaxScaler()

X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

model = keras.Sequential()
model.add(layers.LSTM(50, input_shape=(1, 7)))
# model.add(layers.Dropout(0.2))
# model.add(layers.LSTM(50, return_sequences=True))
# model.add(layers.Dropout(0.2))
# model.add(layers.LSTM(50))
# model.add(layers.Dropout(0.2))
model.add(layers.Dense(1, activation='sigmoid'))
model.compile(optimizer='adam',loss='binary_crossentropy', metrics =['accuracy'])

X_train = X_train.reshape((X_train.shape[0], 1, X_train.shape[1]))
X_test = X_test.reshape((X_test.shape[0], 1, X_test.shape[1]))

model.fit(X_train, y_train, epochs=100, batch_size=32, validation_split=0.1)

model.save("lstm_model.h5")
loss, accuracy = model.evaluate(X_test,y_test)
print(f'Test Accuracy: {accuracy}')