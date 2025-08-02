@echo off
chcp 65001 >nul
title SenaryoNLP - Çağrı Merkezi Asistanı

echo.
echo ============================================================
echo SENARYO NLP - CAGRI MERKEZI ASISTANI
echo ============================================================
echo Uygulama baslatiliyor...
echo ============================================================
echo.

REM Python'un yüklü olup olmadığını kontrol et
python --version >nul 2>&1
if errorlevel 1 (
    echo Python bulunamadi! Lutfen Python'u yukleyin.
    echo https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Gerekli paketleri kontrol et ve yükle
echo Gerekli paketler kontrol ediliyor...
python -c "import flask, fastapi, uvicorn, requests, pydantic" >nul 2>&1
if errorlevel 1 (
    echo Eksik paketler bulundu. Yukleniyor...
    pip install flask fastapi uvicorn requests pydantic
    if errorlevel 1 (
        echo Paket yukleme hatasi!
        pause
        exit /b 1
    )
    echo Paketler yuklendi.
) else (
    echo Tum paketler yuklu.
)

echo.
echo Mock API baslatiliyor...
start "Mock API" cmd /k "python app.py"

echo Web Arayuzu baslatiliyor...
timeout /t 3 /nobreak >nul
start "Web Interface" cmd /k "python web_interface.py"

echo.
echo ============================================================
echo UYGULAMA BASARILI BIR SEKILDE BASLATILDI!
echo ============================================================
echo Web Arayuzu: http://localhost:5000
echo Mock API: http://localhost:8000
echo ============================================================
echo Kullanim:
echo    1. Tarayicinizda http://localhost:5000 adresini acin
echo    2. 'Sesli Konus' butonuna basarak konusmaya baslayin
echo    3. Test musteri ID'leri: 1001, 1002, 1003, 1004, 1005
echo ============================================================
echo Uygulamayi durdurmak icin bu pencereyi kapatın
echo ============================================================
echo.

REM Uygulamaların çalışmasını bekle
echo Uygulamalar calisiyor... (Kapatmak icin Ctrl+C)
pause >nul

echo.
echo Uygulamalar kapatiliyor...
taskkill /f /im python.exe >nul 2>&1
echo Uygulamalar kapatildi.
echo Gorusmek uzere!
pause 