#!/bin/bash

echo "Starting pip environment cleanup..."

# Activate virtual environment if you're using one
# source /path/to/your/venv/bin/activate

# Get a list of all installed packages
INSTALLED_PACKAGES=$(pip freeze)

# Uninstall all packages
echo "Uninstalling all packages..."
if [ -n "$INSTALLED_PACKAGES" ]; then
    echo "$INSTALLED_PACKAGES" | xargs pip uninstall -y
else
    echo "No packages to uninstall."
fi

# Upgrade pip, setuptools, and wheel
echo "Upgrading pip, setuptools, and wheel..."
pip install --upgrade pip setuptools wheel

# Reinstall packages from requirements.txt
if [ -f "requirements.txt" ]; then
    echo "Reinstalling packages from requirements.txt..."
    pip install -r requirements.txt
else
    echo "requirements.txt not found. Skipping package installation."
fi

echo "Pip environment cleanup complete!"

# List installed packages
echo "Current installed packages:"
pip list