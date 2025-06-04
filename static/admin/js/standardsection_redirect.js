document.addEventListener('DOMContentLoaded', function() {
    // If we're on the standard section admin page, redirect to our custom view
    const path = window.location.pathname;
    if (path === '/admin/quality_docs/standardsection/') {
        window.location.href = '/quality_docs/admin/sections/';
    }
});
