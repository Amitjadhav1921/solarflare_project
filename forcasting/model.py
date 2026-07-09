import torch.nn as nn
class FlarePredictor(nn.Module):
 def __init__(self):
  super().__init__(); self.fc=nn.Sequential(nn.Linear(300,64),nn.ReLU(),nn.Linear(64,1),nn.Sigmoid())
 def forward(self,x):
  return self.fc(x.reshape(x.size(0),-1))
