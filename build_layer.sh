#!/bin/bash

set -e

# === Config ===
LAYER_NAME="shared_layer"
PYTHON_VERSION="python"
OUTPUT_ZIP="${LAYER_NAME}.zip"
LAYER_DIR="build_${LAYER_NAME}"

# === Clean previous builds ===
echo "🧹 Cleaning up old builds..."
rm -rf "$LAYER_DIR" "$OUTPUT_ZIP"

# === Create structure ===
echo "📁 Creating layer directory..."
mkdir -p "$LAYER_DIR/$PYTHON_VERSION"

# === Install dependencies ===
echo "📦 Installing packages into layer..."
pip install "openai<1.0.0" requests -t "$LAYER_DIR/$PYTHON_VERSION"

# === Zip the layer ===
echo "📦 Creating zip: $OUTPUT_ZIP"
cd "$LAYER_DIR"
zip -r "../$OUTPUT_ZIP" .
cd ..

# === Final cleanup ===
echo "🧹 Removing temporary build directory..."
rm -rf "$LAYER_DIR"

echo "✅ Done: Created $OUTPUT_ZIP and cleaned up."
