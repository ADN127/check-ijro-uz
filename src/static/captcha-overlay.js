// Captcha Overlay System
class CaptchaOverlay {
    constructor() {
        this.isVerified = false;
        this.overlayElement = null;
        this.captchaWidgetId = null;
        this.init();
    }

    init() {
        // Session tekshiruvi
        this.checkCaptchaStatus();
    }

    async checkCaptchaStatus() {
        // Har safar sahifa yangilanganda captcha so'ralsin
        this.showCaptchaOverlay();
    }

    showCaptchaOverlay() {
        // Overlay yaratish
        this.overlayElement = document.createElement('div');
        this.overlayElement.id = 'captcha-overlay';
        this.overlayElement.innerHTML = `
            <div class="captcha-overlay-backdrop">
                <div class="captcha-overlay-container">
                    <div id="captcha-widget-container"></div>
                    <div class="captcha-error" id="captcha-error" style="display: none;"></div>
                    <div class="captcha-loading" id="captcha-loading" style="display: none;">Tekshirilmoqda...</div>
                </div>
            </div>
        `;

        // CSS qo'shish
        const style = document.createElement('style');
        style.textContent = `
            #captcha-overlay {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                z-index: 10000;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            }
            
            .captcha-overlay-backdrop {
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(255, 255, 255, 0.95);
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 20px;
                box-sizing: border-box;
            }
            
            .captcha-overlay-container {
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
            }
            
            #captcha-widget-container {
                margin-bottom: 20px;
            }
            
            .captcha-error {
                background: #fef2f2;
                border: 1px solid #fecaca;
                color: #dc2626;
                padding: 12px 20px;
                border-radius: 8px;
                font-size: 14px;
                margin-top: 15px;
                text-align: center;
                max-width: 400px;
            }
            
            .captcha-loading {
                color: #374151;
                font-size: 14px;
                margin-top: 15px;
                text-align: center;
            }
        `;

        document.head.appendChild(style);
        document.body.appendChild(this.overlayElement);

        // reCAPTCHA yuklash
        this.loadRecaptcha();
    }

    loadRecaptcha() {
        // reCAPTCHA script yuklash
        if (!window.grecaptcha) {
            const script = document.createElement('script');
            script.src = 'https://www.google.com/recaptcha/api.js?onload=onCaptchaOverlayLoad&render=explicit';
            script.async = true;
            script.defer = true;
            document.head.appendChild(script);
            
            // Global callback
            window.onCaptchaOverlayLoad = () => {
                this.renderCaptcha();
            };
        } else {
            this.renderCaptcha();
        }
    }

    renderCaptcha() {
        const container = document.getElementById('captcha-widget-container');
        if (container && window.grecaptcha) {
            this.captchaWidgetId = grecaptcha.render(container, {
                'sitekey': '6LfmMokrAAAAAFwjS5ZjBsBgwZcjTRlF-05g20FG',
                'callback': (token) => this.onCaptchaSuccess(token),
                'expired-callback': () => this.onCaptchaExpired(),
                'error-callback': () => this.onCaptchaError()
            });
        }
    }

    async onCaptchaSuccess(token) {
        console.log('Captcha success:', token);
        this.showLoading();
        
        try {
            const response = await fetch('/verify_captcha', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    'g-recaptcha-response': token
                })
            });

            const result = await response.json();

            if (response.ok && result.success) {
                this.isVerified = true;
                this.hideCaptchaOverlay();
            } else {
                this.showError(result.error || 'Captcha tekshiruvida xatolik yuz berdi.');
                this.resetCaptcha();
            }
        } catch (error) {
            this.showError('Server bilan bog\'lanishda xatolik: ' + error.message);
            this.resetCaptcha();
        } finally {
            this.hideLoading();
        }
    }

    onCaptchaExpired() {
        this.showError('Captcha muddati tugadi. Iltimos, qayta urinib ko\'ring.');
    }

    onCaptchaError() {
        this.showError('Captcha yuklanishida xatolik. Iltimos, sahifani yangilang.');
    }

    resetCaptcha() {
        if (this.captchaWidgetId !== null && window.grecaptcha) {
            grecaptcha.reset(this.captchaWidgetId);
        }
    }

    showError(message) {
        const errorElement = document.getElementById('captcha-error');
        if (errorElement) {
            errorElement.textContent = message;
            errorElement.style.display = 'block';
        }
    }

    hideError() {
        const errorElement = document.getElementById('captcha-error');
        if (errorElement) {
            errorElement.style.display = 'none';
        }
    }

    showLoading() {
        const loadingElement = document.getElementById('captcha-loading');
        if (loadingElement) {
            loadingElement.style.display = 'block';
        }
        this.hideError();
    }

    hideLoading() {
        const loadingElement = document.getElementById('captcha-loading');
        if (loadingElement) {
            loadingElement.style.display = 'none';
        }
    }

    hideCaptchaOverlay() {
        if (this.overlayElement) {
            this.overlayElement.remove();
            this.overlayElement = null;
        }
    }
}

// Sahifa yuklanganda captcha overlay ni ishga tushirish
document.addEventListener('DOMContentLoaded', function() {
    new CaptchaOverlay();
});

