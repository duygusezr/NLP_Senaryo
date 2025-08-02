/**
 * Sesli Yanıt (Speech Synthesis) Fonksiyonları
 */

class SpeechSynthesis {
    constructor() {
        this.voiceEnabled = true;
        this.voices = [];
        this.turkishVoice = null;
        this.initVoices();
    }

    /**
     * Mevcut sesleri yükler
     */
    initVoices() {
        if ('speechSynthesis' in window) {
            // Mevcut sesleri al
            this.voices = window.speechSynthesis.getVoices();
            this.findTurkishVoice();

            // Sesler yüklenmemişse, yüklendikten sonra kontrol et
            if (this.voices.length === 0) {
                window.speechSynthesis.onvoiceschanged = () => {
                    this.voices = window.speechSynthesis.getVoices();
                    this.findTurkishVoice();
                    console.log('Voices loaded:', this.voices.map(v => `${v.name} (${v.lang})`));
                };
            }
        }
    }

    /**
     * Türkçe ses bulur
     */
    findTurkishVoice() {
        this.turkishVoice = this.voices.find(voice => 
            voice.lang.includes('tr') || voice.lang.includes('TR')
        );
        
        if (this.turkishVoice) {
            console.log('Using Turkish voice:', this.turkishVoice.name);
        } else {
            console.log('No Turkish voice found, using default');
        }
    }

    /**
     * Metni sese çevirir ve çalar
     */
    speak(text) {
        console.log('Speak called with:', text);
        console.log('Voice enabled:', this.voiceEnabled);
        console.log('Speech synthesis available:', 'speechSynthesis' in window);
        
        if (!this.voiceEnabled || !('speechSynthesis' in window)) {
            console.log('Speech synthesis not available or disabled');
            return;
        }
        
        console.log('Speaking:', text);
        
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.lang = 'tr-TR';
        utterance.rate = 0.9;
        utterance.pitch = 1;
        utterance.volume = 1;
        
        // Türkçe ses kullan
        if (this.turkishVoice) {
            utterance.voice = this.turkishVoice;
            console.log('Using Turkish voice:', this.turkishVoice.name);
        } else {
            console.log('No Turkish voice found, using default');
        }
        
        // Event listeners
        utterance.onstart = () => {
            console.log('Speech started');
        };
        
        utterance.onend = () => {
            console.log('Speech ended');
        };
        
        utterance.onerror = (event) => {
            console.error('Speech error:', event.error);
        };
        
        try {
            window.speechSynthesis.speak(utterance);
            console.log('Speech synthesis speak called');
        } catch (error) {
            console.error('Speech synthesis error:', error);
        }
    }

    /**
     * Sesli yanıtı aç/kapat
     */
    toggleVoice() {
        this.voiceEnabled = !this.voiceEnabled;
        console.log('Voice toggled to:', this.voiceEnabled);
        return this.voiceEnabled;
    }

    /**
     * Sesli yanıt durumunu kontrol eder
     */
    isSupported() {
        return 'speechSynthesis' in window;
    }

    /**
     * Sesli yanıtın açık olup olmadığını kontrol eder
     */
    isEnabled() {
        return this.voiceEnabled;
    }

    /**
     * Mevcut sesleri listeler
     */
    getAvailableVoices() {
        return this.voices.map(v => `${v.name} (${v.lang})`);
    }
} 