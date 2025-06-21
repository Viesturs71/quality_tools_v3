/**
 * Main JavaScript for user-facing pages
 */
document.addEventListener('DOMContentLoaded', function() {
    console.log('Main JS loaded');
    
    // Auto-dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert:not(.alert-persistent)');
    if (alerts.length > 0) {
        alerts.forEach(function(alert) {
            setTimeout(function() {
                alert.style.opacity = '0';
                alert.style.transition = 'opacity 0.5s';
                setTimeout(function() {
                    alert.style.display = 'none';
                }, 500);
            }, 5000);
        });
    }
    
    // Add loading state to buttons when forms are submitted
    const forms = document.querySelectorAll('form:not(.no-loading-state)');
    if (forms.length > 0) {
        forms.forEach(function(form) {
            form.addEventListener('submit', function() {
                const buttons = form.querySelectorAll('button[type="submit"]');
                buttons.forEach(function(button) {
                    button.setAttribute('disabled', 'disabled');
                    
                    const originalText = button.innerHTML;
                    button.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Notiek apstrāde...';
                    
                    // In case the form submission takes too long, re-enable after 10 seconds
                    setTimeout(function() {
                        button.removeAttribute('disabled');
                        button.innerHTML = originalText;
                    }, 10000);
                });
            });
        });
    }
});