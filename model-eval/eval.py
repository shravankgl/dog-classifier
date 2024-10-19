import os
import sys
import torch

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

import pytorch_lightning as pl
from datamodule.dog_classifier import DogBreedDataModule
from model.dog_classifier import DogBreedClassifier

def main():
    data_module = DogBreedDataModule(data_dir='./data/dataset')
    data_module.setup()

    num_classes = len(data_module.class_to_idx)
    model = DogBreedClassifier(num_classes=num_classes)

    checkpoint_path = 'checkpoints/dog_breed_classifier-epoch=09-val_loss=0.00.ckpt'
    if os.path.exists(checkpoint_path):
        print(f"Loading model from checkpoint: {checkpoint_path}")
        checkpoint = torch.load(checkpoint_path)
        model.load_state_dict(checkpoint['state_dict'])
    else:
        print(f"Warning: Checkpoint not found at {checkpoint_path}. Using untrained model.")

    trainer = pl.Trainer(accelerator='auto', devices='auto')
    results = trainer.test(model, datamodule=data_module)

    print("\nTest metrics:")
    for k, v in results[0].items():
        print(f"{k}: {v}")

if __name__ == "__main__":
    main()