import os
import sys
import torch
from PIL import Image, ImageDraw, ImageFont
import random
import matplotlib.pyplot as plt

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from torchvision import transforms
from model.dog_classifier import DogBreedClassifier
from datamodule.dog_classifier import DogBreedDataModule

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

    model.eval()

    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])

    idx_to_class = {v: k for k, v in data_module.class_to_idx.items()}

    # Create predictions directory if it doesn't exist
    os.makedirs('predictions', exist_ok=True)

    # Select 10 random images for inference
    all_image_paths = []
    for breed_folder in os.listdir(data_module.data_dir):
        breed_path = os.path.join(data_module.data_dir, breed_folder)
        if os.path.isdir(breed_path):
            image_files = [f for f in os.listdir(breed_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
            all_image_paths.extend([os.path.join(breed_path, img) for img in image_files])

    sample_images = random.sample(all_image_paths, 10)

    for i, img_path in enumerate(sample_images):
        image = Image.open(img_path).convert('RGB')
        input_tensor = transform(image).unsqueeze(0)

        with torch.no_grad():
            output = model(input_tensor)
            probabilities = torch.nn.functional.softmax(output[0], dim=0)
            _, predicted_idx = torch.max(output, 1)
            predicted_class = idx_to_class[predicted_idx.item()]
            confidence = probabilities[predicted_idx].item()

        actual_class = os.path.basename(os.path.dirname(img_path))

        # Create a figure for plotting
        fig, ax = plt.subplots(figsize=(10, 10))
        ax.imshow(image)
        ax.axis('off')
        
        # Add text to the image
        title = f"Actual: {actual_class}\nPredicted: {predicted_class}\nConfidence: {confidence:.2f}"
        ax.text(0.5, -0.1, title, horizontalalignment='center', verticalalignment='center', transform=ax.transAxes, fontsize=12, color='black', bbox=dict(facecolor='white', alpha=0.8))

        # Save the figure
        output_path = f'predictions/sample_{i+1}_prediction.png'
        plt.savefig(output_path, bbox_inches='tight', pad_inches=0.1)
        plt.close()

        print(f"Saved prediction for image {i+1} to {output_path}")

    print("Inference complete. Check the 'predictions' folder for results.")

if __name__ == "__main__":
    main()