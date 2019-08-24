# Import Libraries
import torch
import torch.nn as nn
import numpy as np


class ANNModel(nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim):
        super(ANNModel, self).__init__()
        # Linear function 1: 784 --> 100
        self.fc1 = nn.Linear(input_dim, hidden_dim)
        # Non-linearity 1
        self.relu1 = nn.ReLU()

        # Linear function 2: 100 --> 100
        self.fc2 = nn.Linear(hidden_dim, hidden_dim)
        # Non-linearity 2
        self.tanh2 = nn.Tanh()

        # Linear function 3: 100 --> 100
        self.fc3 = nn.Linear(hidden_dim, hidden_dim)
        # Non-linearity 3
        self.elu3 = nn.ELU()

        # Linear function 4 (readout): 100 --> 10
        self.fc4 = nn.Linear(hidden_dim, output_dim)

    def forward(self, x):
        # Linear function 1
        out = self.fc1(x)
        # Non-linearity 1
        out = self.relu1(out)

        # Linear function 2
        out = self.fc2(out)
        # Non-linearity 2
        out = self.tanh2(out)

        # Linear function 2
        out = self.fc3(out)
        # Non-linearity 2
        out = self.elu3(out)

        # Linear function 4 (readout)
        out = self.fc4(out)
        return out

def get_model():
    # instantiate ANN
    input_dim = 14
    hidden_dim = 150
    output_dim = 1

    # Create ANN
    model = ANNModel(input_dim, hidden_dim, output_dim)

    # Cross Entropy Loss
    error = nn.MSELoss()

    # SGD Optimizer
    learning_rate = 0.02
    optimizer = torch.optim.SGD(model.parameters(), lr=learning_rate)

    model = ANNModel(input_dim, hidden_dim, output_dim)
    model.load_state_dict(torch.load('D:\jaipur\london\model.save'))
    return model


def predict(values):
    val = np.array(values).astype(np.float32)
    val = torch.from_numpy(val).float()
    model = get_model()
    prediction = model(val)
    return int(round(prediction.item(), 4)*1500)


# def euc(x):
#     x = np.array(x)
#     multi = np.array([5, 4, 3, 2])
#     energy = x.dot(multi)
#     similarity = []
#     for i in range(len(df)):
#         row = df.loc[i][:4].values
#         diff = x - row
#         diffsq = diff * diff
#         simval = 1 / (1 + np.sqrt(np.sum(diffsq)))
#         similarity.append(simval)
#     df['similarity'] = similarity
#     df.sort_values(by='similarity', ascending=False, inplace=True)
#     return df.iloc[0]['plans']
#
#
# # input
# h = input("Enter heavy_appliances : ")
# f = input("Fans: ")
# l = input("Lights: ")
# b = input("Bulbs: ")
# x = list(map(int, [h, f, l, b]))
# p = euc(x)
# print(p)