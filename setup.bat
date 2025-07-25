@echo off
echo ===============================================
echo ALICE Bot - Complete Setup Script
echo Author: onex_dv
echo ===============================================

echo [1/5] Creating directory structure...
if not exist "core" mkdir core
if not exist "interface" mkdir interface  
if not exist "credentials" mkdir credentials
if not exist "result" mkdir result

echo [2/5] Installing Python dependencies...
pip install requests>=2.28.0
pip install colorama>=0.4.4
pip install pathlib2>=2.3.0
pip install typing-extensions>=4.0.0

echo [3/5] Verifying installation...
python -c "import requests, colorama; print('Dependencies OK')"

echo [4/5] Running system validation...
python check_system.py

echo [5/5] Setup completed!
echo.
echo ===============================================
echo ALICE Bot Ready for Use!
echo ===============================================
echo.
echo Usage Examples:
echo python base.py sc 0xc51beb5b222aed7f0b56042f04895ee41886b763 p Vv wallet.txt
echo python base.py sc 0xc51beb5b222aed7f0b56042f04895ee41886b763 p Vf addresses.txt
echo python base.py help
echo.
pause
