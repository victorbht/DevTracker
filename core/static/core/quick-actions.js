// DevTracker - Ações Rápidas
// Repetir sessão e edição inline

// 1. Repetir última sessão
function setupRepeatSession() {
    const btnRepeat = document.getElementById('btnRepeatSession');
    if (!btnRepeat) return;
    
    btnRepeat.addEventListener('click', () => {
        const lastRow = document.querySelector('tr.row-view');
        if (!lastRow) return;
        
        const techId = lastRow.getAttribute('data-tech-id');
        const metId = lastRow.getAttribute('data-met-id');
        const topico = lastRow.getAttribute('data-top');
        
        // Preenche o formulário
        const form = document.querySelector('#regModal form');
        if (form) {
            form.querySelector('[name="tecnologia"]').value = techId;
            form.querySelector('[name="metodo"]').value = metId;
            form.querySelector('[name="topico"]').value = topico;
            
            // Abre o modal
            const modal = new bootstrap.Modal(document.getElementById('regModal'));
            modal.show();
            
            // Foca no campo de tempo
            setTimeout(() => document.getElementById('id_tempo_liquido')?.focus(), 300);
        }
    });
}

// 2. Edição inline de tempo
function setupInlineEdit() {
    document.addEventListener('dblclick', (e) => {
        const cell = e.target.closest('td[data-label="Tempo"]');
        if (!cell || cell.querySelector('input')) return;
        
        const row = cell.closest('tr.row-view');
        if (!row) return;
        
        const sessionId = row.getAttribute('data-id');
        const currentTime = cell.textContent.trim();
        const rawTime = row.getAttribute('data-dur-raw');
        
        // Cria input
        const input = document.createElement('input');
        input.type = 'text';
        input.className = 'form-control form-control-sm';
        input.value = rawTime;
        input.style.width = '100px';
        
        const originalContent = cell.innerHTML;
        cell.innerHTML = '';
        cell.appendChild(input);
        input.focus();
        input.select();
        
        const save = async () => {
            const newTime = input.value.trim();
            if (!newTime || !/^\d{1,2}:\d{2}:\d{2}$/.test(newTime)) {
                cell.innerHTML = originalContent;
                return;
            }
            
            // Envia via fetch
            const formData = new FormData();
            formData.append('csrfmiddlewaretoken', document.querySelector('[name=csrfmiddlewaretoken]').value);
            formData.append('tempo_liquido', newTime);
            
            try {
                const response = await fetch(`/editar-tempo/${sessionId}/`, {
                    method: 'POST',
                    body: formData
                });
                
                if (response.ok) {
                    location.reload();
                } else {
                    cell.innerHTML = originalContent;
                }
            } catch (e) {
                cell.innerHTML = originalContent;
            }
        };
        
        const cancel = () => {
            cell.innerHTML = originalContent;
        };
        
        input.addEventListener('blur', save);
        input.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') {
                e.preventDefault();
                save();
            } else if (e.key === 'Escape') {
                e.preventDefault();
                cancel();
            }
        });
    });
}

// Inicializar
document.addEventListener('DOMContentLoaded', () => {
    setupRepeatSession();
    setupInlineEdit();
});

window.DevTrackerQuick = { setupRepeatSession, setupInlineEdit };
