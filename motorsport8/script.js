// Combined JavaScript for Motorsport 8 PDF
// Includes header.js, game-tabs.js, welcome.js

// header.js content
document.addEventListener("DOMContentLoaded", function () {
    const header = document.getElementById("main-header");
    const mainNav = document.getElementById("main-nav");
    const logo = header.querySelector(".logo");
    const mobilePanel = document.getElementById("mobile-panel");

    // Basic mobile menu toggle
    const mobileMenuBtn = document.getElementById("mobile-menu-btn");
    if (mobileMenuBtn) {
        mobileMenuBtn.addEventListener("click", function () {
            mobilePanel.classList.toggle("open");
            mobileMenuBtn.classList.toggle("open");
        });
    }

    // Close mobile panel when clicking outside
    document.addEventListener("click", function (e) {
        if (!header.contains(e.target)) {
            mobilePanel.classList.remove("open");
            if (mobileMenuBtn) mobileMenuBtn.classList.remove("open");
        }
    });

    // Подсветка текущей активной ссылки в навигации хедера
    const navLinks = mainNav ? mainNav.querySelectorAll('.nav-link') : [];
    const currentPath = window.location.pathname.replace(/\/+$/, '');

    function findByPath(prefix) {
        return [...navLinks].find(link => {
            const href = link.getAttribute('href');
            if (!href || href === '#') return false;
            const normalizedHref = href.replace(/\/+$/, '');
            return currentPath === normalizedHref || currentPath.startsWith(normalizedHref + '/') || (normalizedHref === '' && currentPath === '/');
        });
    }

    if (navLinks.length > 0) {
        navLinks.forEach(link => link.classList.remove('active'));

        // Прямое совпадение по URL (где href есть реальный путь)
        let activeLink = findByPath(currentPath);

        // Если не найден, логика для длинных путей /pages/games/forza/etc
        if (!activeLink && currentPath.includes('/pages/games')) {
            activeLink = [...navLinks].find(link => link.textContent.trim().toLowerCase() === 'игры' || link.getAttribute('href') === '#');
        }

        // Посреди специфических страниц
        if (!activeLink) activeLink = findByPath('/pages/main');
        if (!activeLink) activeLink = findByPath('/pages/about');
        if (!activeLink) activeLink = findByPath('/pages/stream');
        if (!activeLink) activeLink = findByPath('/pages/team');
        if (!activeLink) activeLink = findByPath('/pages/partners');

        if (activeLink) {
            activeLink.classList.add('active');
        }
    }
});

// game-tabs.js content
document.addEventListener('DOMContentLoaded', function() {
    const tabButtons = document.querySelectorAll('.game-tab');
    const tabPanes = document.querySelectorAll('.tab-pane');

    if (tabButtons.length === 0 || tabPanes.length === 0) {
        console.warn('Tab elements not found');
        return;
    }

    tabButtons.forEach(button => {
        button.addEventListener('click', function() {
            const targetTab = this.getAttribute('data-tab');

            tabButtons.forEach(btn => {
                btn.classList.remove('active');
            });

            this.classList.add('active');

            tabPanes.forEach(pane => {
                pane.classList.remove('active');
            });

            const targetPane = document.getElementById(targetTab);
            if (targetPane) {
                targetPane.classList.add('active');
            }
        });
    });

    const activeTab = document.querySelector('.game-tab.active');
    if (!activeTab && tabButtons.length > 0) {
        tabButtons[0].click();
    }
});

// welcome.js content (placeholder)
document.addEventListener('DOMContentLoaded', function() {
    // Welcome page specific scripts
    console.log('Welcome scripts loaded');
});