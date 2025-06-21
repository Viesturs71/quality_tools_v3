        document.addEventListener('DOMContentLoaded', function() {
            // Navigācijas izvēlņu loģika
            const dropdownButtons = document.querySelectorAll('.dropdown-button');

            dropdownButtons.forEach(button => {
                const dropdownMenu = button.nextElementSibling;
                const arrow = button.querySelector('.dropdown-arrow');
                const dropdownId = button.id; // Saņem unikālo ID no pogas

                // Pārbaudīt saglabāto stāvokli no localStorage
                const isOpened = localStorage.getItem(`dropdown-${dropdownId}`) === 'true';
                if (isOpened) {
                    dropdownMenu.style.maxHeight = dropdownMenu.scrollHeight + "px";
                    arrow.classList.add('rotate-180');
                }

                button.addEventListener('click', function() {
                    // Pārslēgt izvēlnes redzamību
                    if (dropdownMenu.style.maxHeight) {
                        dropdownMenu.style.maxHeight = null;
                        arrow.classList.remove('rotate-180');
                        localStorage.setItem(`dropdown-${dropdownId}`, 'false'); // Saglabāt aizvērts
                    } else {
                        dropdownMenu.style.maxHeight = dropdownMenu.scrollHeight + "px";
                        arrow.classList.add('rotate-180');
                        localStorage.setItem(`dropdown-${dropdownId}`, 'true'); // Saglabāt atvērts
                    }
                });
            });

            // Tēmas pārslēgšanas funkcionalitāte
            const html = document.documentElement;
            const themeToggle = document.getElementById('toggle-theme');
            const currentThemeSpan = document.getElementById('current-theme');

            function applyTheme(mode) {
                if (mode === 'dark') {
                    html.classList.add('dark');
                    localStorage.setItem('theme', 'dark');
                } else if (mode === 'light') {
                    html.classList.remove('dark');
                    localStorage.setItem('theme', 'light');
                } else {
                    localStorage.removeItem('theme');
                    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
                    html.classList.toggle('dark', prefersDark);
                }
                const active = localStorage.getItem('theme') || 'auto';
                if (currentThemeSpan) currentThemeSpan.textContent = active;
            }

            // Izsaukt tēmas iestatīšanu, kad lapa tiek ielādēta
            applyTheme(localStorage.getItem('theme'));

            if (themeToggle) {
                themeToggle.addEventListener('click', () => {
                    const current = localStorage.getItem('theme') || 'auto';
                    const next = current === 'light' ? 'dark' : current === 'dark' ? 'auto' : 'light';
                    applyTheme(next);
                });
            }
        });
        