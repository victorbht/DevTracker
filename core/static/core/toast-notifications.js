/**
 * Sistema de Toast Notifications Moderno
 * Notificações não-intrusivas com animações suaves
 */

class ToastNotification {
    constructor() {
        this.container = this.createContainer();
        this.queue = [];
        this.isProcessing = false;
    }

    createContainer() {
        let container = document.getElementById('toast-container');
        if (!container) {
            container = document.createElement('div');
            container.id = 'toast-container';
            container.className = 'toast-container';
            document.body.appendChild(container);
        }
        return container;
    }

    show(message, type = 'info', duration = 4000) {
        this.queue.push({ message, type, duration });
        if (!this.isProcessing) {
            this.processQueue();
        }
    }

    async processQueue() {
        if (this.queue.length === 0) {
            this.isProcessing = false;
            return;
        }

        this.isProcessing = true;
        const { message, type, duration } = this.queue.shift();

        const toast = this.createToast(message, type);
        this.container.appendChild(toast);

        // Animação de entrada
        setTimeout(() => toast.classList.add('show'), 10);

        // Auto-remover
        setTimeout(() => {
            this.removeToast(toast);
            this.processQueue();
        }, duration);
    }

    createToast(message, type) {
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;

        const icons = {
            success: '✓',
            error: '✕',
            warning: '⚠',
            info: 'ℹ',
            achievement: '🏆',
            levelup: '⬆️'
        };

        toast.innerHTML = `
            <div class="toast-icon">${icons[type] || icons.info}</div>
            <div class="toast-content">
                <div class="toast-message">${message}</div>
            </div>
            <button class="toast-close" onclick="this.parentElement.remove()">×</button>
        `;

        return toast;
    }

    removeToast(toast) {
        toast.classList.remove('show');
        toast.classList.add('hide');
        setTimeout(() => toast.remove(), 300);
    }

    success(message) {
        this.show(message, 'success');
    }

    error(message) {
        this.show(message, 'error', 5000);
    }

    warning(message) {
        this.show(message, 'warning');
    }

    info(message) {
        this.show(message, 'info');
    }

    achievement(title, xp) {
        const message = `<strong>${title}</strong><br><small>+${xp} XP</small>`;
        this.show(message, 'achievement', 6000);
    }

    levelUp(newLevel) {
        const message = `<strong>Level Up!</strong><br>Agora você é nível ${newLevel}`;
        this.show(message, 'levelup', 6000);
    }
}

// Instância global
const toast = new ToastNotification();

// Estilos CSS (adicionar ao base.html ou criar arquivo separado)
const styles = `
<style>
.toast-container {
    position: fixed;
    top: 20px;
    right: 20px;
    z-index: 9999;
    max-width: 400px;
}

.toast {
    display: flex;
    align-items: center;
    gap: 12px;
    background: white;
    border-radius: 12px;
    padding: 16px;
    margin-bottom: 12px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    border-left: 4px solid #3498db;
    opacity: 0;
    transform: translateX(400px);
    transition: all 0.3s cubic-bezier(0.68, -0.55, 0.265, 1.55);
}

.toast.show {
    opacity: 1;
    transform: translateX(0);
}

.toast.hide {
    opacity: 0;
    transform: translateX(400px);
}

.toast-success {
    border-left-color: #2ecc71;
    background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
}

.toast-error {
    border-left-color: #e74c3c;
    background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%);
}

.toast-warning {
    border-left-color: #f39c12;
    background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%);
}

.toast-info {
    border-left-color: #3498db;
    background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
}

.toast-achievement {
    border-left-color: #9b59b6;
    background: linear-gradient(135deg, #faf5ff 0%, #f3e8ff 100%);
    animation: pulse 0.5s ease-in-out;
}

.toast-levelup {
    border-left-color: #f1c40f;
    background: linear-gradient(135deg, #fefce8 0%, #fef9c3 100%);
    animation: bounce 0.6s ease-in-out;
}

.toast-icon {
    font-size: 24px;
    flex-shrink: 0;
}

.toast-content {
    flex: 1;
    font-size: 14px;
    line-height: 1.5;
}

.toast-message strong {
    font-weight: 600;
    color: #1a1a1a;
}

.toast-close {
    background: none;
    border: none;
    font-size: 20px;
    cursor: pointer;
    color: #666;
    padding: 0;
    width: 24px;
    height: 24px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
    transition: all 0.2s;
}

.toast-close:hover {
    background: rgba(0,0,0,0.1);
    color: #333;
}

@keyframes pulse {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.05); }
}

@keyframes bounce {
    0%, 100% { transform: translateY(0); }
    25% { transform: translateY(-10px); }
    50% { transform: translateY(0); }
    75% { transform: translateY(-5px); }
}

@media (max-width: 768px) {
    .toast-container {
        right: 10px;
        left: 10px;
        max-width: none;
    }
}
</style>
`;

// Adicionar estilos ao documento
if (!document.getElementById('toast-styles')) {
    const styleElement = document.createElement('div');
    styleElement.id = 'toast-styles';
    styleElement.innerHTML = styles;
    document.head.appendChild(styleElement);
}

// Funções helper globais
window.showToast = (message, type) => toast.show(message, type);
window.toastSuccess = (message) => toast.success(message);
window.toastError = (message) => toast.error(message);
window.toastWarning = (message) => toast.warning(message);
window.toastInfo = (message) => toast.info(message);
window.toastAchievement = (title, xp) => toast.achievement(title, xp);
window.toastLevelUp = (level) => toast.levelUp(level);

// Interceptar mensagens do Django e convertê-las em toasts
document.addEventListener('DOMContentLoaded', () => {
    // Mensagens do Django (se existirem)
    const djangoMessages = document.querySelectorAll('.messages .alert, .django-message');
    djangoMessages.forEach(msg => {
        const text = msg.textContent.trim();
        let type = 'info';
        
        if (msg.classList.contains('alert-success') || msg.classList.contains('success')) {
            type = 'success';
        } else if (msg.classList.contains('alert-danger') || msg.classList.contains('error')) {
            type = 'error';
        } else if (msg.classList.contains('alert-warning') || msg.classList.contains('warning')) {
            type = 'warning';
        }
        
        toast.show(text, type);
        msg.style.display = 'none'; // Esconde a mensagem original
    });

    // Detectar novas conquistas via URL params
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.get('success')) {
        toast.success(urlParams.get('success'));
    }
    if (urlParams.get('error')) {
        toast.error(urlParams.get('error'));
    }
});
