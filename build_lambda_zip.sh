#!/bin/bash

# Set variables
PACKAGE_DIR="lambda_package"
ZIP_FILE="lambda_function.zip"
SOURCE_FILE="lambda_function.py"

# Step 1: Clean previous build
echo "Cleaning old package..."
rm -rf "$PACKAGE_DIR" "$ZIP_FILE"

# Step 2: Create package directory
echo "Creating package directory: $PACKAGE_DIR"
mkdir -p "$PACKAGE_DIR"

# Step 3: Copy source file
echo "Copying $SOURCE_FILE into $PACKAGE_DIR"
cp "$SOURCE_FILE" "$PACKAGE_DIR/"

# Step 4: Create ZIP file
echo "Creating zip file: $ZIP_FILE"
cd "$PACKAGE_DIR"
zip -r "../$ZIP_FILE" .
cd ..

echo "✅ Done: Created $ZIP_FILE"
