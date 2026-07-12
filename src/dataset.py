import os
import glob
from PIL import Image
import torch
from torch.utils.data import Dataset, DataLoader
import torchvision.transforms as transforms

class SpatialEuroSATDataset(Dataset):
    def __init__(self, file_list, transform=None):
        self.file_list = file_list
        self.transform = transform

    def __len__(self):
        return len(self.file_list)

    def __getitem__(self, idx):
        img_path, label = self.file_list[idx]
        image = Image.open(img_path).convert('RGB')
        if self.transform:
            image = self.transform(image)
        return image, torch.tensor(label, dtype=torch.long)

def load_eurosat_spatial_splits(data_dir, train_ratio=0.7, val_ratio=0.15):
    classes = sorted([d for d in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, d)) and d != 'allBands'])
    class_to_idx = {cls_name: i for i, cls_name in enumerate(classes)}
    train_records, val_records, test_records = [], [], []

    for cls in classes:
        cls_dir = os.path.join(data_dir, cls)
        files = sorted(glob.glob(os.path.join(cls_dir, "*.jpg")) + glob.glob(os.path.join(cls_dir, "*.png")))
        n_files = len(files)
        n_train = int(n_files * train_ratio)
        n_val = int(n_files * val_ratio)

        for idx, path in enumerate(files):
            record = (path, class_to_idx[cls])
            if idx < n_train: train_records.append(record)
            elif idx < (n_train + n_val): val_records.append(record)
            else: test_records.append(record)

    return train_records, val_records, test_records, classes