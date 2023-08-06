import torch
from torch import nn
from torch.nn import functional


class GlobalPooling(nn.Module):
    def forward(self, x: torch.Tensor):
        return functional.adaptive_avg_pool2d(x, 1)


class Flatten(nn.Module):
    def forward(self, x: torch.Tensor):
        return x.view((x.size(0), -1))


class Classifier(nn.Module):
    def __init__(self, in_features: int, out_features: int, bias: bool = True, dropout: float = 0.0):
        super().__init__()
        self.dropout = dropout
        self.linear = nn.Linear(in_features, out_features, bias=bias)

    def forward(self, x: torch.Tensor):
        if self.dropout:
            x = functional.dropout(x, p=self.dropout, training=self.training, inplace=True)
        return self.linear(x)


class InplaceReLU(nn.ReLU):
    def __init__(self):
        super().__init__(inplace=True)


class InplaceReLU6(nn.ReLU6):
    def __init__(self):
        super().__init__(inplace=True)
