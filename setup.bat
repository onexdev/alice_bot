@echo off
echo ===============================================
echo ALICE Bot - Setup Script
echo Author: onex_dv
echo ===============================================

echo Creating directory structure…
mkdir core 2>nul
mkdir interface 2>nul
mkdir credentials 2>nul
mkdir result 2>nul

echo Installing Python dependencies…
pip install requests>=2.28.0
pip install aiohttp>=3.8.0
pip install colorama>=0.4.4

echo Setup completed successfully!
echo.
echo To run ALICE Bot:
echo python base.py sc WALLET_ADDRESS p Vv output.txt
echo.
echo Example:
echo python base.py sc 0xc51beb5b222aed7f0b56042f04895ee41886b763 p Vv wallet.txt
echo.
pause
