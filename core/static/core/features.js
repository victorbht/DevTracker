// DevTracker - Novas Features
// Estatísticas, Metas e Atalhos de Teclado

// Atalhos de Teclado
document.addEventListener('keydown', (e) => {
    // Ctrl+N ou Cmd+N: Nova sessão
    if ((e.ctrlKey || e.metaKey) && e.key === 'n') {
        e.preventDefault();
        const modal = new bootstrap.Modal(document.getElementById('regModal'));
        modal.show();
    }
    
    // Ctrl+K ou Cmd+K: Busca rápida (foca no filtro de busca)
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        const fullListModal = new bootstrap.Modal(document.getElementById('fullListModal'));
        fullListModal.show();
        setTimeout(() => document.getElementById('filterSearch')?.focus(), 300);
    }
});

// Inicializar
document.addEventListener('DOMContentLoaded', () => {
    // Tooltips para atalhos (discretos)
    const btnNova = document.querySelector('.floating-button');
    if (btnNova && !btnNova.hasAttribute('title')) {
        btnNova.setAttribute('title', 'Atalho: Ctrl+N');
        new bootstrap.Tooltip(btnNova);
    }
    

});

window.DevTrackerFeatures = {};
