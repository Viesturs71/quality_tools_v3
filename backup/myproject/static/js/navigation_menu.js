document.addEventListener('DOMContentLoaded', () => {
    // Atjauno menu-section stāvokli no localStorage
    document.querySelectorAll('.menu-section').forEach(section => {
        const id = section.getAttribute('data-section-id');
        if (localStorage.getItem(`menu-section-${id}`) === 'true') {
            section.classList.remove('collapsed');
        }
    });

    // Atjauno menu-parent stāvokli no localStorage
    document.querySelectorAll('li.menu-parent').forEach(parent => {
        const id = parent.getAttribute('data-parent-id');
        if (localStorage.getItem(`menu-parent-${id}`) === 'true') {
            parent.classList.add('active');
            const symbol = parent.querySelector('.toggle-symbol');
            if (symbol) {
                symbol.textContent = '▼';
                symbol.style.color = '#000'; // aktīvā krāsa
            }
        }
    });

    // Toggle menu-sections ar localStorage saglabāšanu
    document.querySelectorAll('.menu-trigger').forEach(trigger => {
        trigger.style.display = 'flex';
        trigger.style.justifyContent = 'space-between';
        trigger.style.alignItems = 'center';
        
        trigger.addEventListener('click', () => {
            const section = trigger.closest('.menu-section');
            const symbol = trigger.querySelector('.toggle-symbol');
            
            section.classList.toggle('collapsed');
            if (section.classList.contains('collapsed')) {
                symbol.textContent = '▶';
                symbol.style.color = '#6c757d'; // pelēka
            } else {
                symbol.textContent = '▼';
                symbol.style.color = '#000'; // aktīvā krāsa
            }

            const id = section.getAttribute('data-section-id');
            if (id) localStorage.setItem(`menu-section-${id}`, !section.classList.contains('collapsed'));
        });
    });

    // Fix initial state
    document.querySelectorAll('.menu-section').forEach(section => {
        const symbol = section.querySelector('.toggle-symbol');
        if (symbol) {
            if (section.classList.contains('collapsed')) {
                symbol.textContent = '▶';
                symbol.style.color = '#6c757d';
            } else {
                symbol.textContent = '▼';
                symbol.style.color = '#000';
            }
        }
    });

    // Toggle menu-parent ar localStorage saglabāšanu
    document.querySelectorAll('.submenu-trigger').forEach(trigger => {
        trigger.addEventListener('click', (e) => {
            e.preventDefault();
            const parent = trigger.closest('li.menu-parent');
            const symbol = trigger.querySelector('.toggle-symbol');
            parent.classList.toggle('active');
            if (parent.classList.contains('active')) {
                symbol.textContent = '▼';
                symbol.style.color = '#000';
            } else {
                symbol.textContent = '▶';
                symbol.style.color = '#6c757d';
            }
            const id = parent.getAttribute('data-parent-id');
            if (id) localStorage.setItem(`menu-parent-${id}`, parent.classList.contains('active'));
        });
    });

    // Aktīvā izvēlne: atver visus parentus
    const activeLink = document.querySelector('.submenu-content a[href="' + window.location.pathname + '"]');
    if (activeLink) {
        let parent = activeLink.closest('li.menu-parent');
        while (parent) {
            parent.classList.add('active');
            const symbol = parent.querySelector('.toggle-symbol');
            if (symbol) {
                symbol.textContent = '▼';
                symbol.style.color = '#000';
            }
            const id = parent.getAttribute('data-parent-id');
            if (id) localStorage.setItem(`menu-parent-${id}`, true);
            parent = parent.parentElement.closest('li.menu-parent');
        }
        const section = activeLink.closest('.menu-section');
        if (section) {
            section.classList.remove('collapsed');
            const id = section.getAttribute('data-section-id');
            if (id) localStorage.setItem(`menu-section-${id}`, true);
        }
    }

    // Toggle menu-parent (accordion) on trigger click
    document.querySelectorAll('.menu-trigger').forEach(trigger => {
        trigger.addEventListener('click', function(e) {
            e.preventDefault();
            const parent = this.closest('.menu-parent');
            if (parent) {
                parent.classList.toggle('active');
                // Optionally save state in localStorage
                const id = parent.getAttribute('data-parent-id');
                if (id) {
                    localStorage.setItem(`menu-parent-${id}`, parent.classList.contains('active'));
                }
            }
        });
    });

    // Prevent submenu collapse on link click
    document.querySelectorAll('.submenu-content a').forEach(link => {
        link.addEventListener('click', function(e) {
            // Do not remove .active from parent
            // Optionally: highlight the clicked link
            document.querySelectorAll('.submenu-content a.active').forEach(a => a.classList.remove('active'));
            this.classList.add('active');
        });
    });
});
