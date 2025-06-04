/**
 * Admin Navigation Dropdown Functionality
 * Handles the dropdown menu behavior in the admin navigation panel
 */

// Toggle submenu visibility
function toggleSubmenu(button, submenuId) {
    const submenu = document.getElementById(submenuId);
    if (!submenu) return; // Exit if submenu not found
    
    const isExpanded = button.getAttribute('aria-expanded') === 'true';
    
    // Toggle aria attributes
    button.setAttribute('aria-expanded', !isExpanded);
    submenu.setAttribute('aria-hidden', isExpanded);
    
    // Toggle visibility
    submenu.classList.toggle('hidden');
    
    // Rotate chevron icon
    const icon = button.querySelector('.fa-chevron-down');
    if (icon) {
        icon.classList.toggle('rotate-180');
    }
}

// Initialize the dropdown functionality
document.addEventListener('DOMContentLoaded', function() {
    // Add keyboard support
    const buttons = document.querySelectorAll('.nav-dropdown-toggle');
    buttons.forEach(button => {
        // Add click event listener (as a backup for browsers where onclick might not work)
        button.addEventListener('click', function() {
            const submenuId = this.getAttribute('aria-controls');
            if (submenuId) {
                toggleSubmenu(this, submenuId);
            }
        });
        
        // Add keyboard support
        button.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                this.click();
            }
        });
    });
});
