@echo off
chcp 65001 > nul
title NetSpeed Monitor - Build

echo.
echo  ╔══════════════════════════════════════╗
echo  ║   NetSpeed Monitor - Build Script    ║
echo  ╚══════════════════════════════════════╝
echo.

:: Python kontrolü
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo  [HATA] Python bulunamadı! python.org dan indirin.
    pause & exit /b 1
)

:: Bağımlılıkları yükle
echo  [1/4] Bağımlılıklar yükleniyor...
pip install -q -r requirements.txt
if %errorlevel% neq 0 ( echo  HATA! & pause & exit /b 1 )

:: İkon üret
echo  [2/4] İkon oluşturuluyor...
python src/create_icon.py
if %errorlevel% neq 0 ( echo  HATA! & pause & exit /b 1 )

:: EXE derle
echo  [3/4] EXE derleniyor (PyInstaller)...
pyinstaller netspeed.spec --noconfirm
if %errorlevel% neq 0 ( echo  HATA! & pause & exit /b 1 )

:: Installer kontrolü
echo  [4/4] Installer oluşturuluyor (Inno Setup)...
set ISCC="C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
if not exist %ISCC% (
    echo.
    echo  [UYARI] Inno Setup bulunamadı.
    echo  https://jrsoftware.org/isinfo.php adresinden indirin.
    echo  EXE dosyası dist\ klasöründe hazır.
) else (
    %ISCC% installer\setup.iss
    if %errorlevel% neq 0 ( echo  HATA! & pause & exit /b 1 )
    echo.
    echo  ✔ Installer hazır: installer\output\
)

echo.
echo  ════════════════════════════════════════
echo  Build tamamlandı!
echo  EXE:       dist\NetSpeedMonitor.exe
echo  Installer: installer\output\
echo  ════════════════════════════════════════
echo.
pause
