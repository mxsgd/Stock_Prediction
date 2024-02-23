import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import keras
from keras.models import load_model

# Load the saved model
model = load_model("lstm_model.h5")

# Load the new data for which you want to make predictions
new_data = pd.read_csv("new_data.csv")  # Replace "new_data.csv" with the path to your new data file

# Preprocess the new data
new_data.replace([np.inf, -np.inf], np.finfo(np.float64).max, inplace=True)
X_new = new_data[column_names].values

# Scale the new data using the same scaler used during training
scaler = MinMaxScaler()
scaler.fit(X_train)
X_new_scaled = scaler.transform(X_new)

# Reshape the new data to match the input shape expected by the model
X_new_scaled = X_new_scaled.reshape((X_new_scaled.shape[0], 1, X_new_scaled.shape[1]))

# Make predictions
predictions = model.predict(X_new_scaled)

# If you have a classification task, you can get the predicted class for each sample
predicted_classes = np.argmax(predictions, axis=1)

# If you have a regression task, you can get the predicted values
# predicted_values = predictions.flatten()

# Use the predictions as needed for your specific task