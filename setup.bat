@echo off
echo ===============================================
echo ALICE Bot - CRITICAL FIX Setup
echo Author: onex_dv
echo ===============================================

echo [1/3] Installing ONLY required dependencies...
pip install requests>=2.28.0
pip install colorama>=0.4.4

echo [2/3] Verifying installation...
python -c "import requests, json, time; print('Core dependencies OK')"

echo [3/3] Testing colorama (optional)...
python -c "try: import colorama; print('Colorama OK')" "except: print('Colorama missing - colors disabled')"

echo.
echo ===============================================
echo ALICE Bot Ready! Fixed all dependency issues.
echo ===============================================
echo.
echo Test command:
echo python base.py sc 0xc51beb5b222aed7f0b56042f04895ee41886b763 p Vv wallet.txt
echo.
pause
