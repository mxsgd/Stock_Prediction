import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset

class LSTMModel(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(LSTMModel, self).__init__()
        self.lstm = nn.LSTM(input_size,hidden_size, batch_first = True)
        self.fc = nn.Linear(hidden_size, output_size)
        self.sigmoid = nn.Sigmoid()

    def forward(self,x):
        out, _ = self.lstm(x)
        out = self.fc(out[:,-1,:])
        out = self.sigmoid(out)
        return out

data = pd.read_csv("raw_stock_test.csv")

data['Label'] = np.where(data['Close'].shift(-3) > data['Close'], 1, 0)

data = data.drop(data.index[::3034]).reset_index(drop=True)
data = data.dropna()
print(len(data))
data.replace([np.inf, -np.inf], np.finfo(np.float64).max, inplace=True)

features = ['Short_EMA', 'Long_EMA', 'MACD', 'Signal_Line', 'Above', 'Below', 'VolumeToPrice','RS', 'RSI','Lower_Band','Upper_Band']
X = data[features].values
data.to_csv("pre_learning.csv", index=False)
y = data['Label'].values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=48)

scaler = MinMaxScaler()
scaler.fit(X_train)
X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)

X_train = torch.tensor(X_train, dtype=torch.float32)
X_test = torch.tensor(X_test, dtype=torch.float32)
y_train = torch.tensor(y_train, dtype=torch.float32)
y_test = torch.tensor(y_test, dtype=torch.float32)

train_dataset = TensorDataset(X_train, y_train)
train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)

input_size = len(features)
hidden_size = 50
output_size = 1
model = LSTMModel(input_size, hidden_size, output_size)

criterion = nn.BCELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

num_epochs = 10

for epoch in range(num_epochs):
    for inputs, labels in train_loader:
        optimizer.zero_grad()
        outputs = model(inputs.unsqueeze(1))
        loss = criterion(outputs, labels.unsqueeze(1))
        loss.backward()
        optimizer.step()
    print(f'Epoch [{epoch + 1}/{num_epochs}], Loss: {loss.item():.4f}')


with torch.no_grad():
    model.eval()
    test_outputs = model(X_test.unsqueeze(1))
    predicted_labels = (test_outputs >= 0.5).float()
    accuracy = torch.sum(predicted_labels.squeeze() == y_test).item() / len(y_test)
    print(f'Test Accuracy: {accuracy:.4f}')

torch.save(model.state_dict(), "lstm_model_pytorch.pth")