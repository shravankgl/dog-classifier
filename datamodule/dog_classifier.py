import os
import pytorch_lightning as pl
from torch.utils.data import DataLoader, Dataset
from torchvision import transforms
from PIL import Image
from sklearn.model_selection import train_test_split

class DogBreedDataset(Dataset):
    def __init__(self, image_paths, labels, transform=None):
        self.image_paths = image_paths
        self.labels = labels
        self.transform = transform

    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, idx):
        image = Image.open(self.image_paths[idx]).convert('RGB')
        label = self.labels[idx]
        
        if self.transform:
            image = self.transform(image)
        
        return image, label

class DogBreedDataModule(pl.LightningDataModule):
    def __init__(self, data_dir: str = './data/dataset', batch_size: int = 32, val_split: float = 0.2):
        super().__init__()
        self.data_dir = data_dir
        self.batch_size = batch_size
        self.val_split = val_split
        
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])

    def setup(self, stage=None):
        image_paths = []
        labels = []
        self.class_to_idx = {}
        valid_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.tiff')

        for i, breed_folder in enumerate(sorted(os.listdir(self.data_dir))):
            breed_path = os.path.join(self.data_dir, breed_folder)
            if os.path.isdir(breed_path):
                self.class_to_idx[breed_folder] = i
                breed_images = [f for f in os.listdir(breed_path) if f.lower().endswith(valid_extensions)]
                for img_name in breed_images:
                    img_path = os.path.join(breed_path, img_name)
                    image_paths.append(img_path)
                    labels.append(i)

        train_paths, val_paths, train_labels, val_labels = train_test_split(
            image_paths, labels, test_size=self.val_split, stratify=labels, random_state=42
        )

        self.train_dataset = DogBreedDataset(train_paths, train_labels, self.transform)
        self.val_dataset = DogBreedDataset(val_paths, val_labels, self.transform)
        self.test_dataset = self.val_dataset

    def train_dataloader(self):
        return DataLoader(self.train_dataset, batch_size=self.batch_size, shuffle=True, num_workers=4)

    def val_dataloader(self):
        return DataLoader(self.val_dataset, batch_size=self.batch_size, num_workers=4)

    def test_dataloader(self):
        return DataLoader(self.test_dataset, batch_size=self.batch_size, num_workers=4)