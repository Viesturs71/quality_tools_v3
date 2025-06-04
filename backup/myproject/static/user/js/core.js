// Core JS functions for admin-like functionality
'use strict';
{
    const toggleNavSidebar = document.getElementById('toggle-nav-sidebar');
    if (toggleNavSidebar !== null) {
        const navSidebar = document.getElementById('nav-sidebar');
        const main = document.getElementById('main');
        let navSidebarIsOpen = localStorage.getItem('django.admin.navSidebarIsOpen');
        if (navSidebarIsOpen === null) {
            navSidebarIsOpen = 'true';
        }
        
        main.classList.toggle('shifted', navSidebarIsOpen === 'true');
        navSidebar.classList.toggle('closed', navSidebarIsOpen !== 'true');
        
        toggleNavSidebar.addEventListener('click', function() {
            if (navSidebarIsOpen === 'true') {
                navSidebarIsOpen = 'false';
            } else {
                navSidebarIsOpen = 'true';
            }
            localStorage.setItem('django.admin.navSidebarIsOpen', navSidebarIsOpen);
            main.classList.toggle('shifted');
            navSidebar.classList.toggle('closed');
        });
    }
    
    function initFilterSupport() {
        if (document.getElementById('nav-filter')) {
            document.querySelector('#nav-filter').addEventListener('change', function(e) {
                const value = e.target.value.toLowerCase();
                document.querySelectorAll('#nav-sidebar tr').forEach(function(item) {
                    if (item.querySelector('th, td').textContent.trim().toLowerCase().indexOf(value) > -1 || value === '') {
                        item.style.display = 'table-row';
                    } else {
                        item.style.display = 'none';
                    }
                });
            });
            
            document.querySelector('#nav-filter').addEventListener('keyup', function(e) {
                const event = new Event('change');
                e.target.dispatchEvent(event);
            });
        }
    }
    
    document.addEventListener('DOMContentLoaded', function() {
        initFilterSupport();
    });
}
