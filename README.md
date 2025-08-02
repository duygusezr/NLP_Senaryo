# 🎯 SenaryoNLP - Çağrı Merkezi Asistanı

Modern web tabanlı sesli çağrı merkezi asistanı. Gemini AI ile entegre, sesli konuşma ve yanıt özellikli.

## 🚀 Hızlı Başlatma

### Windows için:
```bash
# Çift tıklayın veya komut satırında çalıştırın:
start_app.bat
```

### Python ile:
```bash
python start_app.py
```

## 📋 Gereksinimler

- Python 3.8+
- Flask
- FastAPI
- Uvicorn
- Requests
- Pydantic

## 🔧 Manuel Kurulum

1. **Paketleri yükleyin:**
```bash
pip install flask fastapi uvicorn requests pydantic
```

2. **Mock API'yi başlatın:**
```bash
python app.py
```

3. **Web arayüzünü başlatın:**
```bash
python web_interface.py
```

## 🌐 Kullanım

1. **Web arayüzünü açın:** http://localhost:5000
2. **Sesli konuşma:** "Sesli Konuş" butonuna basın
3. **Sesli yanıt:** "Sesli Yanıt" butonu ile kontrol edin
4. **Test müşteri ID'leri:** 1001, 1002, 1003, 1004, 1005

## 🎯 Özellikler

- ✅ **Sesli Konuşma:** Web Speech API ile ses tanıma
- ✅ **Sesli Yanıt:** Türkçe sesli yanıt
- ✅ **Mock API:** Müşteri bilgileri, paket yönetimi, fatura
- ✅ **Gemini AI:** Gelişmiş yapay zeka yanıtları
- ✅ **Modern UI:** Responsive ve kullanıcı dostu arayüz
- ✅ **Gerçek Zamanlı:** Anlık sesli iletişim

## 📁 Dosya Yapısı

```
SenaryoNLP/
├── app.py                 # Mock API (FastAPI)
├── web_interface.py       # Flask web arayüzü
├── agent_claude3.py       # AI agent (Gemini)
├── start_app.py          # Python başlatma scripti
├── start_app.bat         # Windows başlatma dosyası
├── requirements.txt       # Python bağımlılıkları
├── templates/
│   └── index.html        # Ana web sayfası
└── static/
    ├── css/
    │   └── style.css     # Stil dosyası
    └── js/
        ├── voice-recognition.js    # Ses tanıma
        ├── speech-synthesis.js     # Sesli yanıt
        ├── api-client.js          # API iletişimi
        └── chat-interface.js      # Ana arayüz
```

## 🔧 API Endpoints

### Mock API (Port 8000)
- `GET /getUserInfo/{customer_id}` - Müşteri bilgileri
- `GET /getUsageStats/{customer_id}` - Kullanım istatistikleri
- `GET /getBillingInfo/{customer_id}` - Fatura bilgileri
- `POST /changePackage` - Paket değiştirme

### Web API (Port 5000)
- `POST /api/voice/chat` - Sesli sohbet
- `POST /api/reset` - Konuşma sıfırlama
- `GET /api/status` - API durumu

## 🎮 Test Senaryoları

1. **Müşteri Bilgileri:**
   - "Merhaba, müşteri bilgilerimi öğrenebilir miyim?"
   - Müşteri ID: 1004

2. **Paket Yönetimi:**
   - "Paketimi yükseltmek istiyorum"
   - "Premium pakete geçmek istiyorum"

3. **Kullanım İstatistikleri:**
   - "Kalan haklarım hakkında bilgi almak istiyorum"

4. **Fatura Bilgileri:**
   - "Fatura bilgilerimi bakabilir misin?"

## 🛠️ Sorun Giderme

### Sesli yanıt çalışmıyor:
1. Tarayıcı izinlerini kontrol edin
2. "Test Ses" butonunu deneyin
3. Console hatalarını kontrol edin

### API bağlantı hatası:
1. Her iki servisin de çalıştığından emin olun
2. Port 5000 ve 8000'in açık olduğunu kontrol edin
3. `start_app.bat` ile yeniden başlatın

### Paket hatası:
```bash
pip install -r requirements.txt
```


## 📞 Destek

Sorun yaşarsanız:
1. Console hatalarını kontrol edin (F12)
2. Servislerin çalıştığını doğrulayın
3. Tarayıcı cache'ini temizleyin

## 🎉 Başarı!

Uygulama başarıyla çalıştığında:
- ✅ Mock API: http://localhost:8000
- ✅ Web Arayüzü: http://localhost:5000
- ✅ Sesli konuşma aktif
- ✅ Sesli yanıt aktif

**İyi kullanımlar! 🚀**

## 📝 Son Güncellemeler

### v1.8 - Encoding Sorunu Çözümü
- ✅ Windows'ta emoji karakterleri encoding sorunu çözüldü
- ✅ `web_interface.py` dosyasındaki emoji karakterleri kaldırıldı
- ✅ `start_app.py` dosyasındaki emoji karakterleri kaldırıldı  
- ✅ `start_app.bat` dosyasındaki emoji karakterleri kaldırıldı
- ✅ Artık Windows'ta sorunsuz çalışıyor

### v1.7 - Modüler Yapı
- ✅ HTML/CSS/JS dosyaları ayrıldı
- ✅ Cache busting eklendi
- ✅ Detaylı hata ayıklama logları
- ✅ "Test Ses" butonu eklendi

### v1.6 - Sesli Yanıt İyileştirmeleri
- ✅ Türkçe ses desteği
- ✅ Sesli yanıt açma/kapama
- ✅ Gelişmiş hata yakalama

### v1.5 - Web Arayüzü
- ✅ Sesli konuşma özelliği
- ✅ Web Speech API entegrasyonu
- ✅ Modern responsive tasarım











