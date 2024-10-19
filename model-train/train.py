import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

import pytorch_lightning as pl
from pytorch_lightning.callbacks import ModelCheckpoint
from pytorch_lightning.loggers import TensorBoardLogger
from datamodule.dog_classifier import DogBreedDataModule
from model.dog_classifier import DogBreedClassifier

def main():
    data_module = DogBreedDataModule(data_dir='./data/dataset')
    data_module.setup()

    num_classes = len(data_module.class_to_idx)
    model = DogBreedClassifier(num_classes=num_classes)

    logger = TensorBoardLogger("lightning_logs", name="dog_breed_classifier")
    checkpoint_callback = ModelCheckpoint(
        dirpath='checkpoints',
        filename='dog_breed_classifier-{epoch:02d}-{val_loss:.2f}',
        save_top_k=3,
        monitor='val_loss'
    )

    trainer = pl.Trainer(
        max_epochs=10,
        accelerator='auto',
        devices='auto',
        logger=logger,
        callbacks=[checkpoint_callback],
        log_every_n_steps=10
    )

    trainer.fit(model, data_module)

if __name__ == "__main__":
    main()