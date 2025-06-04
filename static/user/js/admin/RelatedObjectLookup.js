'use strict';
{
    // Simple stub to avoid errors
    window.RelatedObjectLookups = {
        showRelatedObjectLookupPopup: function(triggeringLink) {
            const name = triggeringLink.dataset.modelId;
            const link = triggeringLink.dataset.href || triggeringLink.href;
            if (link) {
                const win = window.open(link, name, 'height=500,width=800,resizable=yes,scrollbars=yes');
                win.focus();
            }
            return false;
        },
        
        dismissRelatedLookupPopup: function(win, chosenId) {
            win.close();
        }
    };
    
    document.addEventListener('DOMContentLoaded', function() {
        document.querySelectorAll('.related-lookup').forEach(function(link) {
            link.addEventListener('click', function(e) {
                e.preventDefault();
                window.RelatedObjectLookups.showRelatedObjectLookupPopup(this);
            });
        });
    });
}
