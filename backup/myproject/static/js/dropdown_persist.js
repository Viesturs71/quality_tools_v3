/**
 * Custom dropdown handler to prevent dropdowns from closing when clicking on items
 * and to ensure they stay open based on the current page URL path.
 */
document.addEventListener('DOMContentLoaded', function() {
    // Completely disable Bootstrap's dropdown behavior
    const dropdownToggles = document.querySelectorAll('.dropdown-toggle');
    
    // Remove Bootstrap's built-in dropdown behavior
    dropdownToggles.forEach(function(toggle) {
        // Remove Bootstrap's data attributes
        toggle.removeAttribute('data-bs-toggle');
        toggle.removeAttribute('data-bs-auto-close');
        
        // Add our own click handler that won't automatically close the dropdown
        toggle.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            const dropdownMenu = this.nextElementSibling;
            if (dropdownMenu && dropdownMenu.classList.contains('dropdown-menu')) {
                // Toggle the dropdown visibility
                const isExpanded = dropdownMenu.classList.contains('show');
                
                if (isExpanded) {
                    dropdownMenu.classList.remove('show');
                    this.setAttribute('aria-expanded', 'false');
                } else {
                    dropdownMenu.classList.add('show');
                    this.setAttribute('aria-expanded', 'true');
                }
            }
        });
    });
    
    // Critical: Stop propagation for ALL clicks inside dropdown menus
    // This prevents clicks from bubbling up and triggering parent handlers
    document.querySelectorAll('.dropdown-menu').forEach(function(menu) {
        menu.addEventListener('click', function(e) {
            e.stopPropagation();
        }, true); // Use capturing phase
    });
    
    // Keep dropdowns open based on current URL path
    function highlightActiveItems() {
        const currentPath = window.location.pathname;
        
        // Find all navigation links
        document.querySelectorAll('.dropdown-menu a').forEach(function(link) {
            const href = link.getAttribute('href');
            
            // Check if this link corresponds to the current page
            if (href && currentPath.includes(href) && href !== '/') {
                // Mark the link as active
                link.classList.add('active');
                
                // Get the parent dropdown menu and keep it open
                const dropdownMenu = link.closest('.dropdown-menu');
                if (dropdownMenu) {
                    dropdownMenu.classList.add('show');
                    
                    // Set the toggle button to expanded state
                    const toggle = dropdownMenu.previousElementSibling;
                    if (toggle && toggle.classList.contains('dropdown-toggle')) {
                        toggle.setAttribute('aria-expanded', 'true');
                        
                        // Also mark the parent nav item as active
                        const parentNavItem = toggle.closest('.nav-item');
                        if (parentNavItem) {
                            parentNavItem.classList.add('active');
                        }
                    }
                }
            }
        });
    }
    
    // Run on page load
    highlightActiveItems();
    
    // Only close dropdowns when clicking outside of any dropdown
    document.addEventListener('click', function(e) {
        // If the click was outside any dropdown
        if (!e.target.closest('.dropdown')) {
            // Close all dropdowns except those containing the active page link
            document.querySelectorAll('.dropdown-menu.show').forEach(function(menu) {
                // Don't close if this menu has an active link
                if (!menu.querySelector('.active')) {
                    menu.classList.remove('show');
                    
                    const toggle = menu.previousElementSibling;
                    if (toggle && toggle.classList.contains('dropdown-toggle')) {
                        toggle.setAttribute('aria-expanded', 'false');
                    }
                }
            });
        }
    });
});
