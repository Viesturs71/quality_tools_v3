document.addEventListener('DOMContentLoaded', function() {
    // Toggle dropdown menus in the admin sidebar
    const dropdownButtons = document.querySelectorAll('.dropdown-button');
    
    dropdownButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Toggle the arrow
            const arrow = this.querySelector('.dropdown-arrow');
            if (arrow) {
                arrow.classList.toggle('rotate-180');
            }
            
            // Toggle the menu visibility
            const menu = this.nextElementSibling;
            if (menu && menu.classList.contains('nav-dropdown-menu')) {
                if (menu.classList.contains('max-h-0')) {
                    menu.classList.remove('max-h-0');
                    menu.classList.add('max-h-screen');
                } else {
                    menu.classList.remove('max-h-screen');
                    menu.classList.add('max-h-0');
                }
            }
        });
    });
    
    // Auto-expand the current section based on URL
    const currentPath = window.location.pathname;
    
    // Open the dropdown for the current page
    dropdownButtons.forEach(button => {
        const menu = button.nextElementSibling;
        if (!menu || !menu.classList.contains('nav-dropdown-menu')) return;
        
        const links = menu.querySelectorAll('a');
        let shouldOpen = false;
        
        links.forEach(link => {
            const href = link.getAttribute('href');
            if (href && currentPath.includes(href)) {
                shouldOpen = true;
                link.classList.add('active');
                link.classList.add('bg-blue-100');
                link.classList.add('dark:bg-blue-900');
            }
        });
        
        if (shouldOpen) {
            // Simulate click to expand the menu
            setTimeout(() => {
                button.click();
            }, 100);
        }
    });
    
    // Theme toggle functionality
    const themeToggle = document.getElementById('toggle-theme');
    if (themeToggle) {
        themeToggle.addEventListener('click', function() {
            document.documentElement.classList.toggle('dark');
            const isDark = document.documentElement.classList.contains('dark');
            localStorage.setItem('theme', isDark ? 'dark' : 'light');
        });
    }
    
    // Initialize theme from local storage or user preference
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {
        document.documentElement.classList.add('dark');
    } else if (savedTheme === 'light') {
        document.documentElement.classList.remove('dark');
    } else if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
        document.documentElement.classList.add('dark');
    }
    
    // Auto-open the dropdown for the current path
    if (currentPath.includes('/admin/auth/')) {
        const authDropdown = document.getElementById('dropdown-auth');
        if (authDropdown && !authDropdown.nextElementSibling.classList.contains('max-h-screen')) {
            setTimeout(() => authDropdown.click(), 100);
        }
    }
});
