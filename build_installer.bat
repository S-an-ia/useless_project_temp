@echo off
setlocal enabledelayedexpansion
title Useless Alarm Clock ? Build Installer

echo.
echo ============================================================
echo   Useless Alarm Clock ? Windows Installer Builder
echo ============================================================
echo.

REM ?? Step 0: Check Python ????????????????????????????????????
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found. Install from https://python.org
    pause
    exit /b 1
)
echo [OK] Python found.

REM ?? Step 1: Check PyInstaller ???????????????????????????????
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo.
    echo [REQUIRED] PyInstaller is not installed.
    echo Please run this command first:
    echo.
    echo     pip install pyinstaller
    echo.
    pause
    exit /b 1
)
echo [OK] PyInstaller found.

REM ?? Step 2: Check Pillow ????????????????????????????????????
pip show pillow >nul 2>&1
if errorlevel 1 (
    echo.
    echo [REQUIRED] Pillow is not installed.
    echo Please run this command first:
    echo.
    echo     pip install pillow
    echo.
    pause
    exit /b 1
)
echo [OK] Pillow found.

REM ?? Step 3: Clean previous build ????????????????????????????
echo.
echo [1/3] Cleaning previous build...
if exist dist   rmdir /s /q dist
if exist build  rmdir /s /q build
if exist Output rmdir /s /q Output
echo       Done.

REM ?? Step 4: Run PyInstaller ?????????????????????????????????
echo.
echo [2/3] Bundling app with PyInstaller (this takes a minute)...
pyinstaller alarm.spec
if errorlevel 1 (
    echo.
    echo [ERROR] PyInstaller failed. Check output above.
    pause
    exit /b 1
)
echo       Done ? exe is in dist\UselessAlarmClock\

REM ?? Step 5: Run Inno Setup ??????????????????????????????????
echo.
echo [3/3] Building installer with Inno Setup...

REM Common Inno Setup install paths
set ISCC=""
if exist "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" (
    set ISCC="C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
)
if exist "C:\Program Files\Inno Setup 6\ISCC.exe" (
    set ISCC="C:\Program Files\Inno Setup 6\ISCC.exe"
)

if %ISCC%=="" (
    echo.
    echo [REQUIRED] Inno Setup 6 not found.
    echo Please install it from: https://jrsoftware.org/isdl.php
    echo Then run this script again.
    echo.
    pause
    exit /b 1
)

%ISCC% installer.iss
if errorlevel 1 (
    echo.
    echo [ERROR] Inno Setup compilation failed. Check output above.
    pause
    exit /b 1
)

echo.
echo ============================================================
echo   SUCCESS!
echo   Installer saved to: Output\UselessAlarmClock_Setup.exe
echo   Share that file with anyone ? they just double-click it!
echo ============================================================
echo.
pause
