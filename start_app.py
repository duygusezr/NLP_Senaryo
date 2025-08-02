#!/usr/bin/env python3
"""
SenaryoNLP - Çağrı Merkezi Asistanı Başlatma Scripti
Bu script hem Mock API'yi hem de Flask web arayüzünü başlatır.
"""

import subprocess
import time
import sys
import os
import signal
import threading
from datetime import datetime

def print_banner():
    """Uygulama başlangıç banner'ını yazdırır"""
    print("=" * 60)
    print("SENARYO NLP - CAGRI MERKEZI ASISTANI")
    print("=" * 60)
    print(f"Baslatma Zamani: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("Uygulama baslatiliyor...")
    print("=" * 60)

def check_dependencies():
    """Gerekli Python paketlerinin yüklü olup olmadığını kontrol eder"""
    required_packages = [
        'flask', 'fastapi', 'uvicorn', 'requests', 'pydantic'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("Eksik paketler bulundu:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\nPaketleri yuklemek icin su komutu calistirin:")
        print("   pip install flask fastapi uvicorn requests pydantic")
        return False
    
    print("Tum gerekli paketler yuklu")
    return True

def start_mock_api():
    """Mock API'yi başlatır"""
    print("Mock API baslatiliyor...")
    try:
        # Mock API'yi başlat
        mock_process = subprocess.Popen(
            [sys.executable, "app.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Başlatma mesajını bekle
        time.sleep(3)
        
        if mock_process.poll() is None:
            print("Mock API basariyla baslatildi (Port: 8000)")
            return mock_process
        else:
            stdout, stderr = mock_process.communicate()
            print(f"Mock API baslatilamadi: {stderr}")
            return None
            
    except Exception as e:
        print(f"Mock API baslatma hatasi: {e}")
        return None

def start_web_interface():
    """Flask web arayüzünü başlatır"""
    print("Web Arayuzu baslatiliyor...")
    try:
        # Flask uygulamasını başlat
        web_process = subprocess.Popen(
            [sys.executable, "web_interface.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Başlatma mesajını bekle
        time.sleep(3)
        
        if web_process.poll() is None:
            print("Web Arayuzu basariyla baslatildi (Port: 5000)")
            return web_process
        else:
            stdout, stderr = web_process.communicate()
            print(f"Web Arayuzu baslatilamadi: {stderr}")
            return None
            
    except Exception as e:
        print(f"Web Arayuzu baslatma hatasi: {e}")
        return None

def print_status():
    """Uygulama durumunu yazdırır"""
    print("\n" + "=" * 60)
    print("UYGULAMA BASARILI BIR SEKILDE BASLATILDI!")
    print("=" * 60)
    print("Web Arayuzu: http://localhost:5000")
    print("Mock API: http://localhost:8000")
    print("=" * 60)
    print("Kullanim:")
    print("   1. Tarayicinizda http://localhost:5000 adresini acin")
    print("   2. 'Sesli Konus' butonuna basarak konusmaya baslayin")
    print("   3. Test musteri ID'leri: 1001, 1002, 1003, 1004, 1005")
    print("=" * 60)
    print("Uygulamayi durdurmak icin Ctrl+C tuslayin")
    print("=" * 60)

def signal_handler(signum, frame):
    """Ctrl+C sinyalini yakalar ve uygulamayı temiz bir şekilde kapatır"""
    print("\nUygulama kapatiliyor...")
    sys.exit(0)

def main():
    """Ana başlatma fonksiyonu"""
    # Sinyal handler'ı ayarla
    signal.signal(signal.SIGINT, signal_handler)
    
    # Banner'ı yazdır
    print_banner()
    
    # Bağımlılıkları kontrol et
    if not check_dependencies():
        return
    
    # Mock API'yi başlat
    mock_process = start_mock_api()
    if not mock_process:
        print("Mock API baslatilamadi. Uygulama kapatiliyor.")
        return
    
    # Web arayüzünü başlat
    web_process = start_web_interface()
    if not web_process:
        print("Web Arayuzu baslatilamadi. Mock API kapatiliyor.")
        mock_process.terminate()
        return
    
    # Durum mesajını yazdır
    print_status()
    
    try:
        # Uygulamaları çalışır durumda tut
        while True:
            # Mock API'nin çalışıp çalışmadığını kontrol et
            if mock_process.poll() is not None:
                print("Mock API durdu!")
                break
            
            # Web arayüzünün çalışıp çalışmadığını kontrol et
            if web_process.poll() is not None:
                print("Web Arayuzu durdu!")
                break
            
            time.sleep(5)
            
    except KeyboardInterrupt:
        print("\nKullanici tarafindan durduruldu.")
    finally:
        # Uygulamaları temiz bir şekilde kapat
        print("Uygulamalar kapatiliyor...")
        
        if mock_process:
            mock_process.terminate()
            mock_process.wait()
            print("Mock API kapatildi")
        
        if web_process:
            web_process.terminate()
            web_process.wait()
            print("Web Arayuzu kapatildi")
        
        print("Uygulama tamamen kapatildi.")

if __name__ == "__main__":
    main() 