from flask import Flask, render_template, request, jsonify, session, send_from_directory
import os
import json
import requests
import logging
import time
from datetime import datetime
from typing import Dict, List, Optional, Any

# Import the agent functionality
from agent_claude3 import VoiceCallCenterAgent, call_gemini_api, parse_tool_call, execute_tool

# -------------------------------------------------------------------
# Flask App Configuration
# -------------------------------------------------------------------
app = Flask(__name__, static_folder='static')
app.secret_key = 'your-secret-key-here'  # Change this in production

# API Configuration
MOCK_API_BASE = "http://localhost:8000"
GEMINI_API_KEY = "AIzaSyAxISLGXPAJLCWB5OJTnpp4q4tmLI9Obas"
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("web-interface")

# -------------------------------------------------------------------
# Web Interface Routes
# -------------------------------------------------------------------

@app.route('/')
def index():
    """Ana sayfa - Web arayüzü"""
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """Chat API endpoint - Metin tabanlı sohbet"""
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({'error': 'Mesaj boş olamaz'}), 400
        
        # Session'dan conversation history'yi al
        if 'conversation_history' not in session:
            session['conversation_history'] = []
        
        # Agent oluştur (voice_mode=False for text only)
        agent = VoiceCallCenterAgent(voice_mode=False)
        agent.conversation_history = session['conversation_history']
        
        # Mesajı işle
        response = agent.process_message(user_message)
        
        # Session'ı güncelle
        session['conversation_history'] = agent.conversation_history
        
        return jsonify({
            'response': response,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Chat error: {e}")
        return jsonify({'error': 'Bir hata oluştu'}), 500

@app.route('/api/voice/chat', methods=['POST'])
def voice_chat():
    """Sesli chat API endpoint"""
    try:
        data = request.get_json()
        user_speech = data.get('speech', '').strip()
        
        if not user_speech:
            return jsonify({'error': 'Ses algılanamadı'}), 400
        
        # Session'dan conversation history'yi al
        if 'conversation_history' not in session:
            session['conversation_history'] = []
        
        # Agent oluştur (voice_mode=True for voice responses)
        agent = VoiceCallCenterAgent(voice_mode=False)  # Web'de voice_mode=False kullanıyoruz
        agent.conversation_history = session['conversation_history']
        
        # Mesajı işle
        response = agent.process_message(user_speech, voice_response=True)
        
        # Session'ı güncelle
        session['conversation_history'] = agent.conversation_history
        
        return jsonify({
            'response': response,
            'speech': response,  # Sesli yanıt için aynı metin
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Voice chat error: {e}")
        return jsonify({'error': 'Sesli sohbet hatası'}), 500

@app.route('/api/reset', methods=['POST'])
def reset_conversation():
    """Konuşma geçmişini sıfırla"""
    try:
        session['conversation_history'] = []
        return jsonify({'message': 'Konuşma geçmişi sıfırlandı'})
    except Exception as e:
        logger.error(f"Reset error: {e}")
        return jsonify({'error': 'Sıfırlama hatası'}), 500

@app.route('/api/voice/start', methods=['POST'])
def start_voice_recording():
    """Ses kaydını başlat"""
    try:
        return jsonify({
            'status': 'recording_started',
            'message': 'Ses kaydı başlatıldı'
        })
    except Exception as e:
        logger.error(f"Voice start error: {e}")
        return jsonify({'error': 'Ses kaydı başlatılamadı'}), 500

@app.route('/api/voice/stop', methods=['POST'])
def stop_voice_recording():
    """Ses kaydını durdur ve işle"""
    try:
        return jsonify({
            'status': 'recording_stopped',
            'message': 'Ses kaydı durduruldu'
        })
    except Exception as e:
        logger.error(f"Voice stop error: {e}")
        return jsonify({'error': 'Ses kaydı durdurulamadı'}), 500

@app.route('/api/status')
def api_status():
    """API durumunu kontrol et"""
    try:
        # Mock API'yi kontrol et
        response = requests.get(f"{MOCK_API_BASE}/getUserInfo/1001", timeout=5)
        mock_api_status = response.status_code == 200
        
        return jsonify({
            'mock_api': 'connected' if mock_api_status else 'disconnected',
            'gemini_api': 'configured',  # API key var mı kontrol et
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"Status check error: {e}")
        return jsonify({
            'mock_api': 'disconnected',
            'gemini_api': 'configured',
            'timestamp': datetime.now().isoformat()
        })

# -------------------------------------------------------------------
# Template Rendering
# -------------------------------------------------------------------

@app.route('/templates/<template_name>')
def serve_template(template_name):
    """Template dosyalarını serve et"""
    return render_template(template_name)

# -------------------------------------------------------------------
# Main Application
# -------------------------------------------------------------------

if __name__ == '__main__':
    print("Web Arayuzu Baslatiliyor...")
    print("http://localhost:5000 adresinden erisebilirsiniz")
    print("Mock API'nin calistigindan emin olun (python app.py)")
    
    app.run(debug=True, host='0.0.0.0', port=5000) 