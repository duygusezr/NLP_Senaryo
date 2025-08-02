# voice_agent.py

import os
import json
import requests
import logging
import threading
import time
import queue
import sys
from typing import Dict, List, Optional, Any
from datetime import datetime

# Voice processing imports
from gtts import gTTS
# from playsound import playsound  # Web arayüzünde kullanılmıyor
# import sounddevice as sd  # Web arayüzünde kullanılmıyor
# from vosk import Model, KaldiRecognizer  # Web arayüzünde kullanılmıyor

# Pydantic for validation
from pydantic import BaseModel, Field

# -------------------------------------------------------------------
# Configuration
# -------------------------------------------------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("voice-call-center-agent")

# API Configuration
MOCK_API_BASE = "http://localhost:8000"
GEMINI_API_KEY = " "  # Your API key
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

# Voice Configuration
VOICE_MODEL_PATH = "model"  # Vosk model path
AUDIO_TEMP_DIR = "temp_audio"
LISTEN_DURATION = 5  # seconds

# Create temp directory for audio files
os.makedirs(AUDIO_TEMP_DIR, exist_ok=True)

# -------------------------------------------------------------------
# Voice Processing Functions
# -------------------------------------------------------------------
class VoiceProcessor:
    def __init__(self, model_path=VOICE_MODEL_PATH):
        self.model_path = model_path
        self.model = None
        self.recognizer = None
        self._init_speech_recognition()
    
    def _init_speech_recognition(self):
        """Ses tanıma modelini başlatır."""
        # Web arayüzünde vosk kullanılmıyor
        logger.info("Web arayüzünde ses tanıma tarayıcı tarafında yapılıyor")
        return True
    
    def text_to_speech(self, text, lang='tr'):
        """Metni sese çevirir ve çalar."""
        try:
            filename = f"{AUDIO_TEMP_DIR}/output_{int(time.time())}.mp3"
            tts = gTTS(text=text, lang=lang, slow=False)
            tts.save(filename)
            
            logger.info(f"🗣️  Asistan: {text}")
            # playsound(filename)  # Web arayüzünde kullanılmıyor
            
            # Dosyayı sil
            try:
                os.remove(filename)
            except:
                pass
                
        except Exception as e:
            logger.error(f"TTS hatası: {e}")
            print(f"Asistan: {text}")  # Fallback to text
    
    def speech_to_text(self, duration=LISTEN_DURATION):
        """Sesi metne çevirir."""
        # Web arayüzünde ses tanıma tarayıcı tarafında yapılıyor
        logger.info("Web arayüzünde ses tanıma tarayıcı tarafında yapılıyor")
        return ""

# -------------------------------------------------------------------
# Tool Definitions (Same as before)
# -------------------------------------------------------------------
AVAILABLE_TOOLS = {
    "get_user_info": {
        "description": "Müşteri bilgilerini getirir (isim, paket, bakiye)",
        "parameters": {
            "customer_id": "string - Müşteri ID'si (örn: 1001)"
        }
    },
    "get_available_packages": {
        "description": "Mevcut paket seçeneklerini listeler",
        "parameters": {
            "customer_id": "string - Müşteri ID'si"
        }
    },
    "change_package": {
        "description": "Müşterinin paketini değiştirir",
        "parameters": {
            "customer_id": "string - Müşteri ID'si",
            "new_package": "string - Yeni paket adı (Bronze, Silver, Gold, Standart, Premium)"
        }
    },
    "get_billing_info": {
        "description": "Müşterinin fatura bilgilerini getirir",
        "parameters": {
            "customer_id": "string - Müşteri ID'si"
        }
    },
    "get_usage_stats": {
        "description": "Müşterinin kullanım istatistiklerini getirir",
        "parameters": {
            "customer_id": "string - Müşteri ID'si"
        }
    },
    "pay_bill": {
        "description": "Fatura ödemesi yapar",
        "parameters": {
            "customer_id": "string - Müşteri ID'si",
            "month": "string - Fatura ayı (YYYY-MM formatında)",
            "amount": "float - Ödeme tutarı"
        }
    }
}

# -------------------------------------------------------------------
# API Helper Functions (Same as before)
# -------------------------------------------------------------------
def make_api_request(endpoint: str, method: str = "GET", data: Dict = None) -> Dict:
    """Mock API'ye istek gönderir ve sonucu döner."""
    url = f"{MOCK_API_BASE}{endpoint}"
    
    try:
        if method == "GET":
            response = requests.get(url, timeout=10)
        elif method == "POST":
            response = requests.post(url, json=data, timeout=10)
        
        if response.status_code == 200:
            return {"success": True, "data": response.json()}
        else:
            error_detail = response.json().get("detail", "Bilinmeyen hata")
            return {"success": False, "error": error_detail, "status_code": response.status_code}
    
    except requests.exceptions.RequestException as e:
        logger.error(f"API request failed: {e}")
        return {"success": False, "error": "Sistem geçici olarak kullanılamıyor"}

def execute_tool(tool_name: str, parameters: Dict) -> str:
    """Araç fonksiyonlarını çalıştırır."""
    
    if tool_name == "get_user_info":
        customer_id = parameters.get("customer_id")
        result = make_api_request(f"/getUserInfo/{customer_id}")
        
        if result["success"]:
            data = result["data"]["data"]
            return f"Müşteri: {data['name']}, Paket: {data['package']}, Bakiye: {data['balance']} TL"
        else:
            return f"Hata: {result['error']}"
    
    elif tool_name == "get_available_packages":
        customer_id = parameters.get("customer_id")
        result = make_api_request(f"/getAvailablePackages/{customer_id}")
        
        if result["success"]:
            packages = result["data"]["data"]
            package_list = []
            for name, info in packages.items():
                features = ", ".join(info["features"])
                package_list.append(f"{name}: {info['price']} TL - {features}")
            return "Mevcut paketler:\n" + "\n".join(package_list)
        else:
            return f"Hata: {result['error']}"
    
    elif tool_name == "change_package":
        customer_id = parameters.get("customer_id")
        new_package = parameters.get("new_package")
        data = {"customer_id": customer_id, "new_package": new_package}
        result = make_api_request("/initiatePackageChange", method="POST", data=data)
        
        if result["success"]:
            return result["data"]["message"]
        else:
            return f"Paket değişikliği başarısız: {result['error']}"
    
    elif tool_name == "get_billing_info":
        customer_id = parameters.get("customer_id")
        result = make_api_request(f"/getBillingInfo/{customer_id}")
        
        if result["success"]:
            bills = result["data"]["data"]["bills"]
            if not bills:
                return "Fatura kaydı bulunamadı."
            
            bill_info = []
            for bill in bills:
                status = "Ödendi" if bill["paid"] else "Ödenmedi"
                bill_info.append(f"{bill['month']}: {bill['amount']} TL - {status}")
            return "Fatura bilgileri:\n" + "\n".join(bill_info)
        else:
            return f"Hata: {result['error']}"
    
    elif tool_name == "get_usage_stats":
        customer_id = parameters.get("customer_id")
        result = make_api_request(f"/getUsageStats/{customer_id}")
        
        if result["success"]:
            stats = result["data"]["data"]
            data_gb = stats["data_mb"] / 1024
            return f"Kullanım: {stats['calls']} dakika arama, {data_gb:.1f} GB internet, {stats['sms']} SMS"
        else:
            return f"Hata: {result['error']}"
    
    elif tool_name == "pay_bill":
        customer_id = parameters.get("customer_id")
        month = parameters.get("month")
        amount = parameters.get("amount")
        data = {"customer_id": customer_id, "month": month, "amount": amount}
        result = make_api_request("/payBill", method="POST", data=data)
        
        if result["success"]:
            return result["data"]["message"]
        else:
            return f"Ödeme başarısız: {result['error']}"
    
    else:
        return f"Bilinmeyen araç: {tool_name}"

# -------------------------------------------------------------------
# Gemini API Integration (Same as before)
# -------------------------------------------------------------------
def call_gemini_api(messages: List[Dict], system_prompt: str = None) -> str:
    """Gemini 2.0 Flash API'yi çağırır."""
    
    if system_prompt:
        full_message = f"{system_prompt}\n\n" + "\n".join([msg["content"] for msg in messages])
    else:
        full_message = "\n".join([msg["content"] for msg in messages])
    
    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": full_message
                    }
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.3,
            "maxOutputTokens": 1000,
        }
    }

    headers = {
        'Content-Type': 'application/json',
        'X-goog-api-key': GEMINI_API_KEY
    }

    try:
        response = requests.post(GEMINI_API_URL, headers=headers, json=payload)
        
        if response.status_code == 200:
            answer = response.json()
            if 'candidates' in answer and len(answer['candidates']) > 0:
                content = answer['candidates'][0].get('content', {})
                if 'parts' in content and len(content['parts']) > 0:
                    return content['parts'][0].get('text', 'Cevap alınamadı')
                else:
                    return 'Yanıt formatı hatalı'
            else:
                return "Yanıt alınamadı"
        else:
            logger.error(f"Gemini API error: {response.status_code}, {response.text}")
            return f"API Hatası: {response.status_code}"
    
    except Exception as e:
        logger.error(f"Gemini API exception: {e}")
        return "Bağlantı hatası oluştu"

def parse_tool_call(response: str) -> Optional[Dict]:
    """LLM yanıtından araç çağrısını parse eder."""
    try:
        if "TOOL_CALL:" in response:
            tool_part = response.split("TOOL_CALL:")[1].split("END_TOOL")[0].strip()
            return json.loads(tool_part)
        return None
    except:
        return None

def format_conversation_history(history: List[Dict]) -> str:
    """Konuşma geçmişini formatlar."""
    formatted = []
    for msg in history[-6:]:
        role = "Müşteri" if msg["role"] == "user" else "Asistan"
        formatted.append(f"{role}: {msg['content']}")
    return "\n".join(formatted)

# -------------------------------------------------------------------
# Voice CallCenterAgent Class
# -------------------------------------------------------------------
class VoiceCallCenterAgent:
    def __init__(self, voice_mode=True):
        self.voice_mode = voice_mode
        self.voice_processor = VoiceProcessor() if voice_mode else None
        self.conversation_history = []
        self.system_prompt = self._create_system_prompt()
        
        if voice_mode and not self.voice_processor.model:
            logger.warning("Ses modu devre dışı - model yüklenemedi")
            self.voice_mode = False
    
    def _create_system_prompt(self) -> str:
        """Sistem prompt'unu oluşturur."""
        tools_info = []
        for tool_name, tool_info in AVAILABLE_TOOLS.items():
            params = ", ".join([f"{k}: {v}" for k, v in tool_info["parameters"].items()])
            tools_info.append(f"- {tool_name}: {tool_info['description']} | Parametreler: {params}")
        
        return f"""Sen Türkçe konuşan bir çağrı merkezi asistanısın. Müşterilere sesli veya yazılı olarak yardımcı oluyorsun.

MEVCUT ARAÇLAR:
{chr(10).join(tools_info)}

ARAÇ KULLANIM FORMATI:
TOOL_CALL: {{"tool": "araç_adı", "parameters": {{"param1": "değer1", "param2": "değer2"}}}}
END_TOOL

KURALLAR:
1. Kısa ve net yanıtlar ver (sesli konuşma için uygun)
2. Her zaman önce müşteri ID'sini sor
3. Samimi ve profesyonel ol
4. Hataları kibar bir şekilde açıkla
5. Sesli konuşmada sayıları açık bir şekilde söyle (1001 -> bin bir)

SESLİ KONUŞMA İPUÇLARI:
- Kısa cümleler kullan
- Teknik terimleri açıkla
- Rakamları açık söyle
- Duraklamalar ekle
"""

    def listen_and_respond(self) -> bool:
        """Ses dinler ve yanıt verir. True = devam, False = çıkış"""
        if not self.voice_mode:
            print("Ses modu aktif değil!")
            return False
        
        print("\n" + "="*50)
        print("🎤 Konuşmaya başlayabilirsiniz...")
        print("('çıkış', 'quit' veya 'sıfırla' diyebilirsiniz)")
        
        # Ses al
        user_speech = self.voice_processor.speech_to_text()
        
        if not user_speech:
            self.voice_processor.text_to_speech("Sizi duyamadım, lütfen tekrar deneyin.")
            return True
        
        # Özel komutları kontrol et
        user_speech_lower = user_speech.lower()
        if any(word in user_speech_lower for word in ['çıkış', 'quit', 'exit', 'kapat']):
            self.voice_processor.text_to_speech("Görüşmek üzere! İyi günler dilerim.")
            return False
        
        if any(word in user_speech_lower for word in ['sıfırla', 'reset', 'yeniden']):
            self.reset_conversation()
            self.voice_processor.text_to_speech("Konuşma geçmişi sıfırlandı. Size nasıl yardımcı olabilirim?")
            return True
        
        # Mesajı işle ve yanıt ver
        try:
            response = self.process_message(user_speech, voice_response=True)
            self.voice_processor.text_to_speech(response)
        except Exception as e:
            logger.error(f"İşlem hatası: {e}")
            self.voice_processor.text_to_speech("Üzgünüm, bir sorun yaşadım. Lütfen tekrar deneyin.")
        
        return True
    
    def process_message(self, user_message: str, voice_response: bool = False) -> str:
        """Kullanıcı mesajını işler ve yanıt döner."""
        
        # Konuşma geçmişine ekle
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })
        
        # Context hazırla
        context = ""
        if len(self.conversation_history) > 1:
            context = f"Önceki konuşma:\n{format_conversation_history(self.conversation_history[:-1])}\n\n"
        
        current_message = f"{context}Müşteri: {user_message}"
        
        # LLM'den yanıt al
        messages = [{"content": current_message}]
        response = call_gemini_api(messages, self.system_prompt)
        
        # Araç çağrısı kontrol et
        tool_call = parse_tool_call(response)
        
        if tool_call:
            tool_name = tool_call.get("tool")
            parameters = tool_call.get("parameters", {})
            
            logger.info(f"🔧 Tool: {tool_name} - Params: {parameters}")
            tool_result = execute_tool(tool_name, parameters)
            
            # Araç sonucunu LLM'e gönder
            follow_up_prompt = "Araç sonucunu kullanarak müşteriye kısa ve net bir yanıt ver." if voice_response else "Araç sonucunu kullanarak müşteriye uygun bir yanıt ver."
            follow_up_message = f"Araç '{tool_name}' sonucu: {tool_result}\n\n{follow_up_prompt}"
            follow_up_response = call_gemini_api([{"content": follow_up_message}], 
                                               "Araç sonucunu kullanarak müşteriye samimi ve profesyonel bir yanıt ver.")
            
            final_response = follow_up_response
        else:
            final_response = response
        
        # Yanıtı temizle
        final_response = final_response.split("TOOL_CALL:")[0].strip()
        final_response = final_response.split("END_TOOL")[0].strip()
        
        # Konuşma geçmişine ekle
        self.conversation_history.append({
            "role": "assistant", 
            "content": final_response
        })
        
        return final_response
    
    def reset_conversation(self):
        """Konuşma geçmişini sıfırlar."""
        self.conversation_history = []

# -------------------------------------------------------------------
# Main Application
# -------------------------------------------------------------------
def main():
    """Ana uygulama."""
    print("🎙️ Sesli Çağrı Merkezi Asistanı (Gemini 2.0 Flash)")
    print("Test müşteri ID'leri: 1001, 1002, 1003, 1004, 1005")
    print("-" * 60)
    
    # Mod seçimi
    print("Hangi modda çalışmak istiyorsunuz?")
    print("1. Sesli mod (STT + TTS)")
    print("2. Metin modu (sadece yazı)")
    
    while True:
        choice = input("Seçiminiz (1/2): ").strip()
        if choice in ['1', '2']:
            break
        print("Lütfen 1 veya 2 seçin.")
    
    voice_mode = (choice == '1')
    
    try:
        agent = VoiceCallCenterAgent(voice_mode=voice_mode)
        print(f"✅ Agent hazır! ({'Sesli' if voice_mode else 'Metin'} mod)")
        
        if voice_mode:
            print("\n🎤 Sesli mod aktif - Konuşarak etkileşim kurabilirsiniz")
            print("Çıkmak için 'çıkış' deyin")
            
            # Hoş geldin mesajı
            agent.voice_processor.text_to_speech("Merhaba! Size nasıl yardımcı olabilirim?")
            
            # Ana döngü
            while True:
                if not agent.listen_and_respond():
                    break
        
        else:
            print("\n⌨️ Metin modu aktif")
            print("Komutlar: 'quit' (çıkış), 'reset' (sıfırla)")
            
            while True:
                user_input = input("\nSiz: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'çıkış', 'q']:
                    print("Görüşmek üzere! 👋")
                    break
                
                if user_input.lower() == 'reset':
                    agent.reset_conversation()
                    print("✅ Konuşma geçmişi sıfırlandı.")
                    continue
                
                if not user_input:
                    continue
                
                try:
                    response = agent.process_message(user_input)
                    print(f"Asistan: {response}")
                except Exception as e:
                    print(f"❌ Hata: {e}")
    
    except Exception as e:
        print(f"❌ Agent başlatılamadı: {e}")
        print("\nGereksinimler:")
        print("1. Mock API çalışıyor olmalı (python app.py)")
        print("2. Sesli mod için Vosk Türkçe modeli 'model' klasöründe olmalı")
        print("3. Gerekli kütüphaneler yüklü olmalı")

if __name__ == "__main__":
    main()
