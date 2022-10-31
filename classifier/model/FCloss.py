import torch.nn as nn
import torch
import torch.nn.functional as F
import numpy as np

class FocalLoss(nn.Module):
    def __init__(self, alpha=-1, gamma=0., class_weight={}, label_smoothing=0., ):
        super(FocalLoss, self).__init__()
        assert gamma >= 0
        self.gamma = gamma
        self.alpha = alpha
        self.bceloss = nn.CrossEntropyLoss(reduction='none', label_smoothing=label_smoothing)
        self.class_weight = class_weight


    def forward(self, input, target):
        # for model overall loss
        weights = 1

        if self.class_weight:
            weights = torch.tensor(list(map(lambda x:self.class_weight[int(x)], target)), device = target.device)
        
        targets = torch.zeros_like(input)
        targets[range(len(input)), target] = 1

        bce_l = self.bceloss(input, targets)
        bce_l = bce_l * weights
        pt = torch.clamp(torch.exp(-bce_l), min=1e-6, max=1-1e-6)
        loss = (torch.pow(1-pt, self.gamma) * bce_l).sum()

        return loss