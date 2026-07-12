import os
import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision.models as models

class FastBaselineCNN(nn.Module):
    def __init__(self, num_classes=10):
        super(FastBaselineCNN, self).__init__()
        self.conv1 = nn.Conv2d(3, 32, kernel_size=3, padding=1)
        self.bn1 = nn.BatchNorm2d(32)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.bn2 = nn.BatchNorm2d(64)
        self.conv3 = nn.Conv2d(64, 64, kernel_size=3, padding=1)
        self.bn3 = nn.BatchNorm2d(64)
        self.pool = nn.MaxPool2d(2, 2)
        self.adaptive_pool = nn.AdaptiveAvgPool2d((4, 4))
        self.fc1 = nn.Linear(64 * 4 * 4, 128)
        self.dropout = nn.Dropout(0.4)
        self.fc2 = nn.Linear(128, num_classes)

    def forward(self, x):
        x = self.pool(F.relu(self.bn1(self.conv1(x))))
        x = self.pool(F.relu(self.bn2(self.conv2(x))))
        x = self.pool(F.relu(self.bn3(self.conv3(x))))
        x = self.adaptive_pool(x)
        x = x.view(x.size(0), -1)
        x = F.relu(self.fc1(x))
        x = self.dropout(x)
        x = self.fc2(x)
        return x

class SpatialEmbeddingExtractor(nn.Module):
    def __init__(self, checkpoint_path=None, device='cpu'):
        super(SpatialEmbeddingExtractor, self).__init__()
        self.backbone = models.resnet18()
        self.backbone.fc = nn.Linear(self.backbone.fc.in_features, 10)
        if checkpoint_path and os.path.exists(checkpoint_path):
            self.backbone.load_state_dict(torch.load(checkpoint_path, map_location=device))
        self.backbone.fc = nn.Identity()
        self.backbone.eval()

    def forward(self, x):
        with torch.no_grad():
            return self.backbone(x)