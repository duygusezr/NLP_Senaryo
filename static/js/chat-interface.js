/**
 * Ana Chat Arayüzü Sınıfı
 */

class ChatInterface {
    constructor() {
        this.voiceButton = document.getElementById('voice-button');
        this.voiceControlButton = document.getElementById('voice-control-button');
        this.resetButton = document.getElementById('reset-button');
        this.chatMessages = document.getElementById('chat-messages');
        
        this.isTyping = false;
        
        // Modüller
        this.voiceRecognition = new VoiceRecognition();
        this.speechSynthesis = new SpeechSynthesis();
        this.apiClient = new ApiClient();
        
        this.initializeEventListeners();
        this.initializeVoiceRecognition();
        this.checkApiStatus();
        this.setupPeriodicStatusCheck();
        this.checkVoiceSupport();
    }

    /**
     * Event listener'ları başlatır
     */
    initializeEventListeners() {
        // Voice button click
        this.voiceButton.addEventListener('click', () => {
            this.toggleVoiceRecording();
        });

        // Reset button click
        this.resetButton.addEventListener('click', () => {
            this.resetConversation();
        });

        // Voice control button click
        this.voiceControlButton.addEventListener('click', () => {
            this.toggleVoiceResponse();
        });

        // Test voice button click
        const testVoiceButton = document.getElementById('test-voice-button');
        if (testVoiceButton) {
            testVoiceButton.addEventListener('click', () => {
                this.testVoiceResponse();
            });
        }
    }

    /**
     * Ses tanıma modülünü başlatır
     */
    initializeVoiceRecognition() {
        this.voiceRecognition.setCallbacks(
            // onResult
            (transcript) => {
                this.addMessage(transcript, 'user');
                this.processVoiceChat(transcript);
            },
            // onError
            (errorMessage) => {
                this.addErrorMessage(errorMessage);
                this.stopVoiceRecording();
            },
            // onStart
            () => {
                this.addMessage('🎤 Konuşmaya başlayabilirsiniz...', 'assistant');
            },
            // onEnd
            () => {
                this.stopVoiceRecording();
            }
        );
    }

    /**
     * Ses kaydını başlat/durdur
     */
    toggleVoiceRecording() {
        if (this.voiceRecognition.isRecording) {
            this.stopVoiceRecording();
        } else {
            this.startVoiceRecording();
        }
    }

    /**
     * Ses kaydını başlatır
     */
    startVoiceRecording() {
        this.voiceButton.classList.add('recording');
        this.voiceButton.innerHTML = '<i class="fas fa-stop"></i><span>Kaydı Durdur</span>';
        this.voiceButton.title = 'Kaydı durdur';
        this.voiceRecognition.startRecognition();
    }

    /**
     * Ses kaydını durdurur
     */
    stopVoiceRecording() {
        this.voiceButton.classList.remove('recording');
        this.voiceButton.innerHTML = '<i class="fas fa-microphone"></i><span>Sesli Konuş</span>';
        this.voiceButton.title = 'Ses ile konuş';
        this.voiceRecognition.stopRecognition();
    }

    /**
     * Sesli sohbet mesajını işler
     */
    async processVoiceChat(speech) {
        try {
            console.log('Processing voice chat:', speech);
            this.showTypingIndicator();

            const result = await this.apiClient.sendVoiceMessage(speech);
            console.log('Voice chat result:', result);

            this.hideTypingIndicator();

            if (result.success) {
                console.log('Voice chat successful, response:', result.response);
                this.addMessage(result.response, 'assistant');
                
                // Sesli yanıtı kontrol et
                if (this.speechSynthesis.isEnabled()) {
                    console.log('Speaking response:', result.speech);
                    this.speechSynthesis.speak(result.speech);
                } else {
                    console.log('Voice response disabled, not speaking');
                }
            } else {
                console.error('Voice chat failed:', result.error);
                this.addErrorMessage(result.error);
            }
        } catch (error) {
            console.error('Voice chat error:', error);
            this.hideTypingIndicator();
            this.addErrorMessage('Sesli sohbet bağlantı hatası');
        }
    }

    /**
     * Sesli yanıtı aç/kapat
     */
    toggleVoiceResponse() {
        const isEnabled = this.speechSynthesis.toggleVoice();
        
        if (isEnabled) {
            this.voiceControlButton.classList.remove('muted');
            this.voiceControlButton.innerHTML = '<i class="fas fa-volume-up"></i><span>Sesli Yanıt</span>';
            this.voiceControlButton.title = 'Sesli yanıtı kapat';
            this.addMessage('🔊 Sesli yanıt açıldı', 'assistant');
            
            // Test sesi çal
            this.speechSynthesis.speak('Sesli yanıt aktif');
            console.log('Voice response enabled');
        } else {
            this.voiceControlButton.classList.add('muted');
            this.voiceControlButton.innerHTML = '<i class="fas fa-volume-mute"></i><span>Sesli Yanıt</span>';
            this.voiceControlButton.title = 'Sesli yanıtı aç';
            this.addMessage('🔇 Sesli yanıt kapatıldı', 'assistant');
            console.log('Voice response disabled');
        }
    }

    /**
     * Sesli yanıt test fonksiyonu
     */
    testVoiceResponse() {
        console.log('Testing voice response...');
        this.addMessage('🔊 Test sesi çalınıyor...', 'assistant');
        this.speechSynthesis.speak('Bu bir test sesidir. Sesli yanıt çalışıyor.');
    }

    /**
     * Konuşma geçmişini sıfırlar
     */
    async resetConversation() {
        try {
            console.log('Resetting conversation...');
            const result = await this.apiClient.resetConversation();
            console.log('Reset result:', result);

            if (result.success) {
                // Clear all messages except welcome message
                const messages = this.chatMessages.querySelectorAll('.message');
                console.log('Found messages:', messages.length);
                
                messages.forEach(msg => {
                    const content = msg.querySelector('.message-content');
                    if (content) {
                        const text = content.textContent;
                        // Sadece welcome message'ı koru
                        if (!text.includes('Merhaba! Ben çağrı merkezi asistanınızım')) {
                            console.log('Removing message:', text.substring(0, 50) + '...');
                            msg.remove();
                        }
                    }
                });
                
                // Add reset confirmation
                this.addMessage('✅ Konuşma geçmişi sıfırlandı', 'assistant');
                console.log('Reset completed successfully');
            } else {
                console.error('Reset failed:', result.error);
                this.addErrorMessage('Konuşma sıfırlanamadı: ' + (result.error || 'Bilinmeyen hata'));
            }
        } catch (error) {
            console.error('Reset error:', error);
            this.addErrorMessage('Sıfırlama hatası: ' + error.message);
        }
    }

    /**
     * API durumunu kontrol eder
     */
    async checkApiStatus() {
        try {
            const status = await this.apiClient.checkApiStatus();
            this.updateStatusIndicator('mock-api-status', status.mock_api);
            this.updateStatusIndicator('gemini-api-status', status.gemini_api);
        } catch (error) {
            this.updateStatusIndicator('mock-api-status', 'disconnected');
            this.updateStatusIndicator('gemini-api-status', 'disconnected');
        }
    }

    /**
     * Durum göstergesini günceller
     */
    updateStatusIndicator(elementId, status) {
        const element = document.getElementById(elementId);
        const icon = element.querySelector('i');
        const text = element.querySelector('span');

        if (status === 'connected' || status === 'configured') {
            element.className = 'status-item status-connected';
            icon.className = 'fas fa-circle';
            text.textContent = text.textContent.split(' ')[0] + ' API';
        } else {
            element.className = 'status-item status-disconnected';
            icon.className = 'fas fa-circle';
            text.textContent = text.textContent.split(' ')[0] + ' API';
        }
    }

    /**
     * Periyodik durum kontrolü
     */
    setupPeriodicStatusCheck() {
        this.apiClient.setupPeriodicStatusCheck((status) => {
            this.updateStatusIndicator('mock-api-status', status.mock_api);
            this.updateStatusIndicator('gemini-api-status', status.gemini_api);
        });
    }

    /**
     * Ses desteğini kontrol eder
     */
    checkVoiceSupport() {
        if (this.speechSynthesis.isSupported()) {
            console.log('Speech synthesis supported');
            this.addMessage('🔊 Sesli yanıt hazır', 'assistant');
        } else {
            console.log('Speech synthesis not supported');
            this.addErrorMessage('❌ Tarayıcınız sesli yanıt özelliğini desteklemiyor');
        }
    }

    /**
     * Mesaj ekler
     */
    addMessage(content, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}`;

        const avatar = document.createElement('div');
        avatar.className = 'message-avatar';
        avatar.innerHTML = sender === 'user' ? '<i class="fas fa-user"></i>' : '<i class="fas fa-robot"></i>';

        const messageContent = document.createElement('div');
        messageContent.className = 'message-content';
        messageContent.textContent = content;

        const messageTime = document.createElement('div');
        messageTime.className = 'message-time';
        messageTime.textContent = new Date().toLocaleTimeString('tr-TR', { 
            hour: '2-digit', 
            minute: '2-digit' 
        });

        messageContent.appendChild(messageTime);
        messageDiv.appendChild(avatar);
        messageDiv.appendChild(messageContent);

        this.chatMessages.appendChild(messageDiv);
        this.scrollToBottom();
    }

    /**
     * Hata mesajı ekler
     */
    addErrorMessage(error) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-message';
        errorDiv.innerHTML = `<i class="fas fa-exclamation-triangle"></i> ${error}`;
        this.chatMessages.appendChild(errorDiv);
        this.scrollToBottom();
    }

    /**
     * Yazıyor göstergesini gösterir
     */
    showTypingIndicator() {
        this.isTyping = true;

        const typingDiv = document.createElement('div');
        typingDiv.className = 'message assistant typing-indicator';
        typingDiv.id = 'typing-indicator';
        
        const avatar = document.createElement('div');
        avatar.className = 'message-avatar';
        avatar.innerHTML = '<i class="fas fa-robot"></i>';

        const content = document.createElement('div');
        content.className = 'message-content';
        content.innerHTML = `
            <span>Yazıyor</span>
            <div class="typing-dots">
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
            </div>
        `;

        typingDiv.appendChild(avatar);
        typingDiv.appendChild(content);
        this.chatMessages.appendChild(typingDiv);
        this.scrollToBottom();
    }

    /**
     * Yazıyor göstergesini gizler
     */
    hideTypingIndicator() {
        this.isTyping = false;
        const typingIndicator = document.getElementById('typing-indicator');
        if (typingIndicator) {
            typingIndicator.remove();
        }
    }

    /**
     * Sohbet alanını en alta kaydırır
     */
    scrollToBottom() {
        this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
    }
} 