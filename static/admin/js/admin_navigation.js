// Admin navigation functionality for Quality Tools

document.addEventListener('DOMContentLoaded', function() {
    // Make sections collapsible
    const sections = document.querySelectorAll('.admin-section');
    
    sections.forEach(function(section) {
        section.addEventListener('click', function() {
            const sectionId = this.getAttribute('data-section');
            const content = document.getElementById(sectionId + '-content');
            const icon = this.querySelector('.toggle-icon');
            
            // Toggle this section
            content.classList.toggle('open');
            
            // Update icon
            if (content.classList.contains('open')) {
                icon.classList.remove('fa-chevron-down');
                icon.classList.add('fa-chevron-up');
            } else {
                icon.classList.remove('fa-chevron-up');
                icon.classList.add('fa-chevron-down');
            }
        });
    });
    
    // Open the section if it contains the current URL path
    const currentPath = window.location.pathname;
    
    sections.forEach(function(section) {
        const sectionId = section.getAttribute('data-section');
        const content = document.getElementById(sectionId + '-content');
        const links = content.querySelectorAll('a');
        
        links.forEach(function(link) {
            if (currentPath.includes(link.getAttribute('href'))) {
                content.classList.add('open');
                const icon = section.querySelector('.toggle-icon');
                icon.classList.remove('fa-chevron-down');
                icon.classList.add('fa-chevron-up');
            }
        });
    });
});
