/**
 * API İletişim Fonksiyonları
 */

class ApiClient {
    constructor() {
        this.baseUrl = 'http://localhost:5000';
    }

    /**
     * API durumunu kontrol eder
     */
    async checkApiStatus() {
        try {
            const response = await fetch(`${this.baseUrl}/api/status`);
            const data = await response.json();
            return {
                mock_api: data.mock_api,
                gemini_api: data.gemini_api
            };
        } catch (error) {
            console.error('API status check failed:', error);
            return {
                mock_api: 'disconnected',
                gemini_api: 'disconnected'
            };
        }
    }

    /**
     * Sesli sohbet mesajı gönderir
     */
    async sendVoiceMessage(speech) {
        try {
            console.log('Sending voice message:', speech);
            const response = await fetch(`${this.baseUrl}/api/voice/chat`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ speech: speech })
            });

            console.log('Voice chat response status:', response.status);
            console.log('Voice chat response headers:', response.headers);
            
            // Response text'ini önce al
            const responseText = await response.text();
            console.log('Voice chat response text:', responseText);
            
            let data;
            try {
                data = JSON.parse(responseText);
                console.log('Voice chat response data:', data);
            } catch (parseError) {
                console.error('JSON parse error:', parseError);
                console.error('Response text was:', responseText);
                return {
                    success: false,
                    error: 'Geçersiz JSON yanıtı: ' + responseText.substring(0, 100)
                };
            }

            if (response.ok) {
                return {
                    success: true,
                    response: data.response,
                    speech: data.speech,
                    timestamp: data.timestamp
                };
            } else {
                console.error('Voice chat API error:', data.error);
                return {
                    success: false,
                    error: data.error || 'Sesli sohbet hatası'
                };
            }
        } catch (error) {
            console.error('Voice chat network error:', error);
            return {
                success: false,
                error: 'Sesli sohbet bağlantı hatası: ' + error.message
            };
        }
    }

    /**
     * Konuşma geçmişini sıfırlar
     */
    async resetConversation() {
        try {
            console.log('Sending reset request...');
            const response = await fetch(`${this.baseUrl}/api/reset`, {
                method: 'POST'
            });

            console.log('Reset response status:', response.status);
            const data = await response.json();
            console.log('Reset response data:', data);

            return {
                success: response.ok,
                message: data.message,
                error: data.error
            };
        } catch (error) {
            console.error('Reset error:', error);
            return {
                success: false,
                error: 'Sıfırlama hatası: ' + error.message
            };
        }
    }

    /**
     * Periyodik durum kontrolü
     */
    setupPeriodicStatusCheck(callback, interval = 30000) {
        setInterval(async () => {
            try {
                const status = await this.checkApiStatus();
                callback(status);
            } catch (error) {
                console.error('Periodic status check failed:', error);
                callback({
                    mock_api: 'disconnected',
                    gemini_api: 'disconnected'
                });
            }
        }, interval);
    }
} 