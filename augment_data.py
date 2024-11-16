import os
import cv2
import random
import numpy as np
from sklearn.model_selection import train_test_split
from torchvision import transforms
from PIL import Image

def load_img_paths(folder_path):
    return [os.path.join(folder_path, fname) for fname in os.listdir(folder_path) if fname.endswith(('.jpg', '.png', '.jpeg'))]

def apply_augmentation_and_save(img_path, save_dir, augmentations=5):

    # Define augmentation pipeline
    augmentation_pipeline = transforms.Compose([
        transforms.RandomHorizontalFlip(),
        transforms.RandomRotation(30),
        transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2, hue=0.1)
    ])

    img = cv2.imread(img_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(img)

    # Apply augmentations and save
    for i in range(augmentations):
        augmented_img = augmentation_pipeline(pil_image)
        augmented_img = np.array(augmented_img)  
        augmented_img = cv2.cvtColor(augmented_img, cv2.COLOR_RGB2BGR)  

        # Create save path
        base_name = os.path.basename(img_path)
        name, ext = os.path.splitext(base_name)
        augmented_save_path = os.path.join(save_dir, f"{name}_aug_{i}{ext}")
        
        # Save augmented image
        cv2.imwrite(augmented_save_path, augmented_img)

def main():
    dataset_dir = "dataset"
    augmented_dataset_dir = "augmented_dataset"

    marigold = load_img_paths(os.path.join(dataset_dir, 'marigold'))
    sunflower = load_img_paths(os.path.join(dataset_dir, 'sunflower'))

    marigold = list(zip(marigold, [0] * len(marigold)))
    sunflower = list(zip(sunflower, [1] * len(sunflower)))
    dataset = marigold + sunflower

    # Train-test split with stratification
    _, labels = zip(*dataset)
    train, test = train_test_split(dataset, test_size=0.2, stratify=labels)

    # Create directories for augmented dataset
    train_dir = os.path.join(augmented_dataset_dir, "train")
    test_dir = os.path.join(augmented_dataset_dir, "test")
    os.makedirs(train_dir, exist_ok=True)
    os.makedirs(test_dir, exist_ok=True)

    # Save test data
    for img_path, label in test:
        label_dir = os.path.join(test_dir, "marigold" if label == 0 else "sunflower")
        os.makedirs(label_dir, exist_ok=True)
        save_path = os.path.join(label_dir, os.path.basename(img_path))
        cv2.imwrite(save_path, cv2.imread(img_path))  # Save original test image

    # Save and augment training data
    for img_path, label in train:
        label_dir = os.path.join(train_dir, "marigold" if label == 0 else "sunflower")
        os.makedirs(label_dir, exist_ok=True)
        save_path = os.path.join(label_dir, os.path.basename(img_path))

        # Save original image
        cv2.imwrite(save_path, cv2.imread(img_path))

        # Apply augmentations and save
        apply_augmentation_and_save(img_path, label_dir, augmentations=5)

    print("Augmented dataset created successfully!")

if __name__ == "__main__":
    main()
