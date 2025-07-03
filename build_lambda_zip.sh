#!/bin/bash

set -e

# === Config ===
DIST_DIR="dist"
LAMBDA_DIRS=("summarize_bulletin" "download_bulletin" "delete_bulletins")

# === Prepare dist folder ===
mkdir -p "$DIST_DIR"
rm -f "$DIST_DIR"/*.zip

for DIR in "${LAMBDA_DIRS[@]}"; do
  echo "📦 Building Lambda: $DIR"

  TEMP_DIR="build_$DIR"
  rm -rf "$TEMP_DIR"
  mkdir -p "$TEMP_DIR"

  # Copy source files
  cp "$DIR/lambda_function.py" "$TEMP_DIR/"

  # Install dependencies if requirements.txt exists
  if [ -f "$DIR/requirements.txt" ]; then
    echo "📦 Installing dependencies for $DIR..."
    pip install -r "$DIR/requirements.txt" -t "$TEMP_DIR/"
  fi

  # Zip the Lambda
  (cd "$TEMP_DIR" && zip -r "../$DIST_DIR/${DIR}.zip" .)

  echo "✅ Done: $DIST_DIR/${DIR}.zip"

  rm -rf "$TEMP_DIR"
done
