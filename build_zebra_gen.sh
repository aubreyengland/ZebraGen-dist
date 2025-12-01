#!/usr/bin/env bash
set -euo pipefail

# Move to the script's directory (project root)
cd "$(dirname "$0")"

echo ">>> Cleaning previous build artifacts..."
rm -rf build dist zebra_gen.spec

echo ">>> Running PyInstaller..."
pyinstaller \
  --onefile \
  --name zebra_gen \
  --paths zebra_gen_client \
  zebra_gen.py

echo ">>> Copying JSON resources beside the executable..."
cp dept_info.json dist/
cp site_info.json dist/
cp env_template.txt dist/
# If needed later, you can also copy enve_template.txt:
# cp enve_template.txt dist/

echo ">>> Build complete."
echo "Executable: dist/zebra_gen"
echo "JSON files: dist/dept_info.json, dist/site_info.json"
echo "Environment template: dist/env_template.txt"
echo "You can now distribute the 'dist' directory."
