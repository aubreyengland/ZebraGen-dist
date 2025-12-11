@echo off
setlocal

REM Move to the script's directory (project root)
cd /d "%~dp0"

echo ">>> Cleaning previous build artifacts..."
if exist "build" ( rd /s /q build )
if exist "dist" ( rd /s /q dist )
if exist "zebra_gen.spec" ( del zebra_gen.spec )

echo ">>> Running PyInstaller..."
pyinstaller ^
  --onefile ^
  --name zebra_gen ^
  --add-data "dept_info.json;." ^
  --add-data "site_info.json;." ^
  --add-data "env_template.txt;." ^
  --paths "zebra_gen_client" ^
  zebra_gen.py

echo ">>> Build complete."
echo "Executable: dist\zebra_gen.exe"
echo "You can now distribute the 'dist' directory."

endlocal
