document.addEventListener('DOMContentLoaded', function() {
    // Check if we're on the standards section admin page
    if (window.location.pathname.includes('/admin/standards/standardsection/')) {
        // Add a helper message at the top of the page
        var contentMain = document.querySelector('.content-main');
        if (contentMain) {
            var helper = document.createElement('div');
            helper.className = 'helper-message';
            helper.style.padding = '10px';
            helper.style.marginBottom = '15px';
            helper.style.backgroundColor = '#f8f9fa';
            helper.style.border = '1px solid #e5e7eb';
            helper.style.borderRadius = '0.25rem';
            helper.style.fontFamily = '"Times New Roman", Times, serif';
            
            helper.innerHTML = '<p><strong>Migration Helper:</strong> If you encounter database errors, run <code>python manage.py fix_standards_migrations</code> to fix migration issues.</p>';
            
            contentMain.insertBefore(helper, contentMain.firstChild);
        }
    }
});
