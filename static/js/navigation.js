/**
 * Navigation Dropdown Functionality
 * Handles the sidebar section dropdowns
 */

class NavigationDropdowns {
    constructor() {
        this.sectionHeaders = document.querySelectorAll('.sidebar-section');
        this.initDropdowns();
        this.expandActiveSection();
    }
    
    initDropdowns() {
        this.sectionHeaders.forEach(header => {
            header.addEventListener('click', () => this.toggleDropdown(header));
        });
    }
    
    toggleDropdown(header) {
        const sectionName = header.getAttribute('data-section');
        const dropdown = document.getElementById(`${sectionName}-dropdown`);
        
        if (!dropdown) return;
        
        const isActive = dropdown.classList.contains('active');
        
        // Close other dropdowns first
        this.closeAllDropdowns(`${sectionName}-dropdown`);
        
        // Toggle current dropdown
        if (isActive) {
            dropdown.classList.remove('active');
            header.classList.remove('active');
        } else {
            dropdown.classList.add('active');
            header.classList.add('active');
        }
    }
    
    closeAllDropdowns(exceptId) {
        document.querySelectorAll('.sidebar-dropdown.active').forEach(dropdown => {
            if (dropdown.id !== exceptId) {
                dropdown.classList.remove('active');
                const sectionHeader = document.querySelector(`[data-section="${dropdown.id.split('-')[0]}"]`);
                if (sectionHeader) {
                    sectionHeader.classList.remove('active');
                }
            }
        });
    }
    
    expandActiveSection() {
        // Auto-expand the section that contains the active link
        const activeLink = document.querySelector('.sidebar-link.active');
        if (activeLink) {
            const parentDropdown = activeLink.closest('.sidebar-dropdown');
            if (parentDropdown) {
                parentDropdown.classList.add('active');
                const sectionHeader = document.querySelector(`[data-section="${parentDropdown.id.split('-')[0]}"]`);
                if (sectionHeader) {
                    sectionHeader.classList.add('active');
                }
            }
        }
    }
}

// Initialize when the DOM is fully loaded
document.addEventListener('DOMContentLoaded', () => {
    new NavigationDropdowns();
});
