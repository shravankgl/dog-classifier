from setuptools import setup, find_packages

setup(
    name="dog_breed_classifier",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "torch>=1.12.1",
        "torchvision>=0.13.1",
        "pytorch-lightning>=1.6.5",
        "pandas>=1.3.5,<2.0.0",
        "matplotlib>=3.3.0",
        "scikit-learn>=0.24.0",
        "kaggle>=1.5.12",
    ],
)