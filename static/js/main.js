// Main JavaScript for Library Management System

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    initializeTooltips();
    
    // Initialize form validation
    initializeFormValidation();
    
    // Initialize search functionality
    initializeSearch();
    
    // Initialize confirmation dialogs
    initializeConfirmations();
    
    // Initialize auto-refresh for overdue items
    initializeAutoRefresh();
});

/**
 * Initialize Bootstrap tooltips
 */
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

/**
 * Initialize form validation
 */
function initializeFormValidation() {
    // Add real-time validation to forms
    const forms = document.querySelectorAll('form[novalidate]');
    
    forms.forEach(function(form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        });
        
        // Real-time validation for inputs
        const inputs = form.querySelectorAll('input, select, textarea');
        inputs.forEach(function(input) {
            input.addEventListener('blur', function() {
                if (input.checkValidity()) {
                    input.classList.remove('is-invalid');
                    input.classList.add('is-valid');
                } else {
                    input.classList.remove('is-valid');
                    input.classList.add('is-invalid');
                }
            });
        });
    });
    
    // ISBN validation
    const isbnInputs = document.querySelectorAll('input[name="isbn"]');
    isbnInputs.forEach(function(input) {
        input.addEventListener('input', function() {
            validateISBN(input);
        });
    });
}

/**
 * Validate ISBN format
 */
function validateISBN(input) {
    const isbn = input.value.replace(/[-\s]/g, '');
    const isValid = isbn.length === 0 || isbn.length === 10 || isbn.length === 13;
    
    if (isValid || isbn.length === 0) {
        input.setCustomValidity('');
    } else {
        input.setCustomValidity('El ISBN debe tener 10 o 13 dígitos');
    }
}

/**
 * Initialize search functionality
 */
function initializeSearch() {
    const searchInputs = document.querySelectorAll('input[type="search"], input[name="q"]');
    
    searchInputs.forEach(function(input) {
        // Add search icon
        if (!input.parentElement.querySelector('.search-icon')) {
            input.style.paddingLeft = '2.5rem';
            const icon = document.createElement('i');
            icon.className = 'fas fa-search search-icon';
            icon.style.cssText = 'position: absolute; left: 0.75rem; top: 50%; transform: translateY(-50%); color: #6c757d; z-index: 10;';
            input.parentElement.style.position = 'relative';
            input.parentElement.insertBefore(icon, input);
        }
        
        // Add clear button for non-empty searches
        if (input.value.trim()) {
            addClearButton(input);
        }
        
        input.addEventListener('input', function() {
            if (input.value.trim()) {
                addClearButton(input);
            } else {
                removeClearButton(input);
            }
        });
    });
}

/**
 * Add clear button to search input
 */
function addClearButton(input) {
    if (input.parentElement.querySelector('.clear-search')) return;
    
    const clearBtn = document.createElement('button');
    clearBtn.type = 'button';
    clearBtn.className = 'btn-close clear-search';
    clearBtn.style.cssText = 'position: absolute; right: 0.75rem; top: 50%; transform: translateY(-50%); z-index: 10;';
    clearBtn.addEventListener('click', function() {
        input.value = '';
        input.dispatchEvent(new Event('input'));
        input.focus();
    });
    
    input.parentElement.appendChild(clearBtn);
    input.style.paddingRight = '2.5rem';
}

/**
 * Remove clear button from search input
 */
function removeClearButton(input) {
    const clearBtn = input.parentElement.querySelector('.clear-search');
    if (clearBtn) {
        clearBtn.remove();
        input.style.paddingRight = '';
    }
}

/**
 * Initialize confirmation dialogs
 */
function initializeConfirmations() {
    // Delete confirmations
    const deleteButtons = document.querySelectorAll('button[type="submit"][class*="danger"], form[action*="delete"] button[type="submit"]');
    
    deleteButtons.forEach(function(button) {
        button.addEventListener('click', function(event) {
            const confirmMsg = button.getAttribute('data-confirm') || '¿Estás seguro de que quieres eliminar este elemento?';
            if (!confirm(confirmMsg)) {
                event.preventDefault();
                return false;
            }
        });
    });
    
    // Return book confirmations
    const returnButtons = document.querySelectorAll('form[action*="return"] button[type="submit"]');
    
    returnButtons.forEach(function(button) {
        button.addEventListener('click', function(event) {
            if (!confirm('¿Confirmas la devolución de este libro?')) {
                event.preventDefault();
                return false;
            }
        });
    });
}

/**
 * Initialize auto-refresh for overdue items
 */
function initializeAutoRefresh() {
    // Check for overdue loans every 5 minutes
    if (window.location.pathname.includes('loans') || window.location.pathname.includes('dashboard')) {
        setInterval(function() {
            updateOverdueStatus();
        }, 5 * 60 * 1000); // 5 minutes
    }
}

/**
 * Update overdue status indicators
 */
function updateOverdueStatus() {
    const now = new Date();
    const dueDateElements = document.querySelectorAll('[data-due-date]');
    
    dueDateElements.forEach(function(element) {
        const dueDate = new Date(element.getAttribute('data-due-date'));
        const timeDiff = dueDate - now;
        const daysDiff = Math.ceil(timeDiff / (1000 * 60 * 60 * 24));
        
        // Remove existing classes
        element.classList.remove('text-success', 'text-warning', 'text-danger');
        
        if (daysDiff < 0) {
            element.classList.add('text-danger');
            element.textContent = 'Vencido';
        } else if (daysDiff <= 2) {
            element.classList.add('text-warning');
            element.textContent = `${daysDiff} días restantes`;
        } else {
            element.classList.add('text-success');
            element.textContent = `${daysDiff} días restantes`;
        }
    });
}

/**
 * Show loading state on form submission
 */
function showLoadingState(button) {
    button.classList.add('loading');
    button.disabled = true;
    
    // Re-enable after 3 seconds as fallback
    setTimeout(function() {
        button.classList.remove('loading');
        button.disabled = false;
    }, 3000);
}

/**
 * Utility function to format dates
 */
function formatDate(date) {
    return new Intl.DateTimeFormat('es-ES', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit'
    }).format(date);
}

/**
 * Utility function to show toast notifications
 */
function showToast(message, type = 'info') {
    // Create toast container if it doesn't exist
    let toastContainer = document.querySelector('.toast-container');
    if (!toastContainer) {
        toastContainer = document.createElement('div');
        toastContainer.className = 'toast-container position-fixed top-0 end-0 p-3';
        document.body.appendChild(toastContainer);
    }
    
    // Create toast element
    const toastEl = document.createElement('div');
    toastEl.className = `toast align-items-center text-white bg-${type} border-0`;
    toastEl.setAttribute('role', 'alert');
    toastEl.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">${message}</div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
        </div>
    `;
    
    toastContainer.appendChild(toastEl);
    
    // Initialize and show toast
    const toast = new bootstrap.Toast(toastEl);
    toast.show();
    
    // Remove toast element after it's hidden
    toastEl.addEventListener('hidden.bs.toast', function() {
        toastEl.remove();
    });
}

/**
 * Handle AJAX form submissions
 */
function handleAjaxForm(formSelector, successCallback) {
    const forms = document.querySelectorAll(formSelector);
    
    forms.forEach(function(form) {
        form.addEventListener('submit', function(event) {
            event.preventDefault();
            
            const formData = new FormData(form);
            const submitButton = form.querySelector('button[type="submit"]');
            
            showLoadingState(submitButton);
            
            fetch(form.action, {
                method: form.method,
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showToast(data.message, 'success');
                    if (successCallback) successCallback(data);
                } else {
                    showToast(data.message || 'Error al procesar la solicitud', 'danger');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showToast('Error de conexión', 'danger');
            })
            .finally(() => {
                submitButton.classList.remove('loading');
                submitButton.disabled = false;
            });
        });
    });
}

// Export functions for use in other scripts
window.LibrarySystem = {
    showToast,
    formatDate,
    showLoadingState,
    handleAjaxForm
};
