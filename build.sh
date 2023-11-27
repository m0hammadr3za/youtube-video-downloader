#!/bin/bash

# Build the executable
pyinstaller --onefile \
            --noconsole \
            script.py

# Rename the .exe file
mv dist/script.exe dist/script.exe

# Create "Youtube video downloader" directory if it doesn't exist
mkdir -p "Youtube video downloader"

# Move the renamed .exe file to the "Youtube video downloader" directory
mv dist/shamsi-time.exe "Youtube video downloader"/

# Cleanup
rm -rf build dist script.spec

echo "Build complete!"
