/**
 * Ses Tanıma (Speech Recognition) Fonksiyonları
 */

class VoiceRecognition {
    constructor() {
        this.recognition = null;
        this.isRecording = false;
        this.onResultCallback = null;
        this.onErrorCallback = null;
        this.onStartCallback = null;
        this.onEndCallback = null;
    }

    /**
     * Ses tanıma başlatır
     */
    startRecognition() {
        try {
            // Web Speech API kontrolü
            if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
                throw new Error('Tarayıcınız ses tanıma özelliğini desteklemiyor');
            }

            this.isRecording = true;
            this.recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
            this.recognition.lang = 'tr-TR';
            this.recognition.continuous = false;
            this.recognition.interimResults = false;

            // Event listeners
            this.recognition.onstart = () => {
                console.log('🎤 Ses tanıma başladı');
                if (this.onStartCallback) this.onStartCallback();
            };

            this.recognition.onresult = (event) => {
                const transcript = event.results[0][0].transcript;
                console.log('🎯 Algılanan:', transcript);
                if (this.onResultCallback) this.onResultCallback(transcript);
            };

            this.recognition.onerror = (event) => {
                console.error('Speech recognition error:', event.error);
                let errorMessage = this.getErrorMessage(event.error);
                if (this.onErrorCallback) this.onErrorCallback(errorMessage);
            };

            this.recognition.onend = () => {
                console.log('🎤 Ses tanıma bitti');
                if (this.isRecording) {
                    this.stopRecognition();
                }
                if (this.onEndCallback) this.onEndCallback();
            };

            this.recognition.start();

        } catch (error) {
            console.error('Voice recording error:', error);
            if (this.onErrorCallback) this.onErrorCallback('Ses kaydı başlatılamadı');
            this.stopRecognition();
        }
    }

    /**
     * Ses tanımayı durdurur
     */
    stopRecognition() {
        try {
            this.isRecording = false;
            if (this.recognition) {
                this.recognition.stop();
            }
        } catch (error) {
            console.error('Stop recording error:', error);
        }
    }

    /**
     * Hata mesajlarını Türkçe'ye çevirir
     */
    getErrorMessage(error) {
        switch(error) {
            case 'not-allowed':
                return 'Mikrofon izni verilmedi. Lütfen tarayıcı ayarlarından mikrofon iznini verin.';
            case 'no-speech':
                return 'Ses algılanamadı. Lütfen daha net konuşun.';
            case 'audio-capture':
                return 'Mikrofon erişim hatası. Lütfen mikrofonunuzu kontrol edin.';
            case 'network':
                return 'Ağ bağlantı hatası. İnternet bağlantınızı kontrol edin.';
            default:
                return `Ses tanıma hatası: ${error}`;
        }
    }

    /**
     * Callback fonksiyonlarını ayarlar
     */
    setCallbacks(onResult, onError, onStart, onEnd) {
        this.onResultCallback = onResult;
        this.onErrorCallback = onError;
        this.onStartCallback = onStart;
        this.onEndCallback = onEnd;
    }
} 