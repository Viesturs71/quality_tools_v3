/**
 * Custom JavaScript for the Django admin interface
 */
document.addEventListener('DOMContentLoaded', function() {
    console.log('Admin JS loaded');
    
    // Confirm deletions with a custom confirmation dialog
    const deleteButtons = document.querySelectorAll('input[name="_delete"]');
    if (deleteButtons.length > 0) {
        deleteButtons.forEach(function(button) {
            button.addEventListener('click', function(e) {
                if (!confirm('Vai tiešām vēlaties dzēst šo ierakstu? Šo darbību nevarēs atsaukt.')) {
                    e.preventDefault();
                }
            });
        });
    }
    
    // Add a "back to top" button when scrolling down
    const body = document.querySelector('body');
    let backToTopButton = document.createElement('button');
    backToTopButton.textContent = '↑ Augšup';
    backToTopButton.className = 'back-to-top';
    backToTopButton.style.display = 'none';
    backToTopButton.style.position = 'fixed';
    backToTopButton.style.bottom = '20px';
    backToTopButton.style.right = '20px';
    backToTopButton.style.zIndex = '1000';
    backToTopButton.style.padding = '8px 12px';
    backToTopButton.style.backgroundColor = '#3498db';
    backToTopButton.style.color = '#fff';
    backToTopButton.style.border = 'none';
    backToTopButton.style.borderRadius = '4px';
    backToTopButton.style.cursor = 'pointer';
    
    body.appendChild(backToTopButton);
    
    backToTopButton.addEventListener('click', function() {
        window.scrollTo({top: 0, behavior: 'smooth'});
    });
    
    window.addEventListener('scroll', function() {
        if (window.pageYOffset > 300) {
            backToTopButton.style.display = 'block';
        } else {
            backToTopButton.style.display = 'none';
        }
    });
    
    // Highlight required fields more prominently
    const requiredFields = document.querySelectorAll('.required');
    requiredFields.forEach(field => {
        const label = field.querySelector('label');
        if (label) {
            label.style.fontWeight = 'bold';
            if (!label.querySelector('.required-indicator')) {
                const indicator = document.createElement('span');
                indicator.className = 'required-indicator';
                indicator.textContent = ' *';
                indicator.style.color = '#e74c3c';
                label.appendChild(indicator);
            }
        }
    });
});
