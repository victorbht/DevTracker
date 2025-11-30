// DevTracker - Melhorias Implementadas
// 5 melhorias rápidas para UX

// 1. Botão excluir no modal de detalhes
function setupDeleteButton(sessionId) {
    const btnDelete = document.getElementById('btnDeleteFromDetail');
    if (!btnDelete) return;
    
    btnDelete.onclick = async () => {
        if (await confirmDelete('esta sessão')) {
            showLoading();
            const form = document.createElement('form');
            form.method = 'POST';
            form.action = `/excluir/${sessionId}/`;
            const csrf = document.querySelector('[name=csrfmiddlewaretoken]');
            if (csrf) form.appendChild(csrf.cloneNode());
            document.body.appendChild(form);
            form.submit();
        }
    };
}

// 2. Loading spinner
function showLoading() {
    if (document.getElementById('loadingSpinner')) return;
    const spinner = document.createElement('div');
    spinner.id = 'loadingSpinner';
    spinner.style.cssText = 'position:fixed;top:50%;left:50%;transform:translate(-50%,-50%);z-index:9999;';
    spinner.innerHTML = '<div class="spinner-border" style="color:var(--accent);" role="status"></div>';
    document.body.appendChild(spinner);
}

function hideLoading() {
    document.getElementById('loadingSpinner')?.remove();
}

// 3. Confirmação de exclusão
async function confirmDelete(itemName) {
    return new Promise((resolve) => {
        const existing = document.getElementById('confirmDeleteModal');
        if (existing) existing.remove();
        
        const modal = document.createElement('div');
        modal.id = 'confirmDeleteModal';
        modal.className = 'modal fade show';
        modal.style.cssText = 'display:block;background:rgba(0,0,0,0.7);';
        modal.innerHTML = `
            <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content border-0 card-slim">
                    <div class="modal-body text-center p-4">
                        <i class="fas fa-exclamation-triangle text-warning fa-3x mb-3"></i>
                        <h4 class="mb-3 text-white">Confirmar exclusão</h4>
                        <p class="text-muted-2">Deseja realmente excluir ${itemName}?</p>
                        <div class="d-flex gap-2 justify-content-center mt-4">
                            <button class="btn btn-outline-light" id="btnNo">Cancelar</button>
                            <button class="btn btn-danger px-4" id="btnYes">Sim, excluir</button>
                        </div>
                    </div>
                </div>
            </div>
        `;
        document.body.appendChild(modal);
        
        document.getElementById('btnNo').onclick = () => { modal.remove(); resolve(false); };
        document.getElementById('btnYes').onclick = () => { modal.remove(); resolve(true); };
    });
}

// 4. Validação de formulários
function validateTimeFormat(value) {
    return /^(\d{1,2}):([0-5]\d):([0-5]\d)$/.test(value);
}

function setupFormValidation() {
    ['regModal', 'formEdit'].forEach(formId => {
        const form = document.getElementById(formId) || document.querySelector(`#${formId}`);
        if (!form) return;
        
        form.addEventListener('submit', (e) => {
            const tempoInput = form.querySelector('[name="tempo_liquido"]');
            const exInput = form.querySelector('[name="qtd_exercicios"]');
            const acInput = form.querySelector('[name="qtd_acertos"]');
            
            let errors = [];
            
            if (tempoInput && tempoInput.value && !validateTimeFormat(tempoInput.value)) {
                errors.push('Tempo inválido. Use formato HH:MM:SS');
                tempoInput.classList.add('is-invalid');
            } else if (tempoInput) {
                tempoInput.classList.remove('is-invalid');
            }
            
            if (exInput && acInput) {
                const ex = parseInt(exInput.value) || 0;
                const ac = parseInt(acInput.value) || 0;
                if (ac > ex && ex > 0) {
                    errors.push('Acertos não pode ser maior que exercícios');
                    acInput.classList.add('is-invalid');
                } else {
                    acInput.classList.remove('is-invalid');
                }
            }
            
            if (errors.length > 0) {
                e.preventDefault();
                alert(errors.join('\n'));
            }
        });
    });
}

// 5. Interceptar exclusões de tech/método
document.addEventListener('click', async (e) => {
    const link = e.target.closest('a[href*="/excluir/"]');
    if (!link || link.closest('#delModal')) return;
    
    e.preventDefault();
    const itemName = link.closest('li')?.textContent.trim().split('\n')[0] || 'este item';
    
    if (await confirmDelete(itemName)) {
        showLoading();
        window.location.href = link.href;
    }
});

// Inicializar
document.addEventListener('DOMContentLoaded', () => {
    setupFormValidation();
    
    // Adicionar botão excluir no modal de detalhes
    const detailFooter = document.querySelector('#detailModal .card-slim .d-flex');
    if (detailFooter && !document.getElementById('btnDeleteFromDetail')) {
        const btnDel = document.createElement('button');
        btnDel.id = 'btnDeleteFromDetail';
        btnDel.className = 'btn btn-sm btn-danger rounded-pill px-3';
        btnDel.innerHTML = '<i class="fas fa-trash me-1"></i>Excluir';
        detailFooter.appendChild(btnDel);
    }
});

window.DevTracker = { showLoading, hideLoading, confirmDelete, setupDeleteButton };
