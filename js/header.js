document.addEventListener("DOMContentLoaded", function () {
    const header = document.getElementById("main-header");
    const mainNav = document.getElementById("main-nav");
    const logo = header.querySelector(".logo");
    const mobilePanel = document.getElementById("mobile-panel");

    // СОСТОЯНИЕ ПРИЛОЖЕНИЯ - управление стеком меню
    const menuStack = [];
    const MENU_STATES = {
        MAIN: "main",
        GAMES: "games",
        FORZA: "forza",
        AC: "ac",
        PC: "pc"
    };

    // Определяем текущую страницу
    const path = window.location.pathname;
    const currentPage = path.split("/").pop() || "index.html";

    // Фикс маршрутов CSS/JS для локальных сред и github-подпапок, например:
    // /sotikdima1975-star.github.io/new/about/index.html
    // /sotikdima1975-star.github.io/pages/main/index.html
    function getRootPrefix() {
        const knownPrefixes = ["/sotikdima1975-star.github.io/new", "/sotikdima1975-star.github.io"];
        for (const prefix of knownPrefixes) {
            if (path.startsWith(prefix)) {
                return prefix;
            }
        }

        // Если сайт в корне, ставим пустой префикс
        return "";
    }

    const rootPrefix = getRootPrefix();

    function normalizeLinkHref(selector, targetPath) {
        const link = document.querySelector(selector);
        if (link) {
            link.setAttribute("href", rootPrefix + targetPath);
        }
    }

    function prefixPath(href) {
        if (!href || typeof href !== 'string') return href;
        if (href.startsWith('//')) return href;
        if (!href.startsWith('/')) return href;
        const normalized = rootPrefix ? rootPrefix + href : href;
        if (href.startsWith(rootPrefix + '/')) return href;
        return normalized;
    }

    function applyPrefixToNavLinks() {
        document.querySelectorAll('#main-nav a, #mobile-panel a').forEach(link => {
            const href = link.getAttribute('href');
            const prefixed = prefixPath(href);
            link.setAttribute('href', prefixed);
        });
    }

    normalizeLinkHref('link[href="/css/header.css"]', "/css/header.css");
    normalizeLinkHref('link[href="/css/welcome.css"]', "/css/welcome.css");
    applyPrefixToNavLinks();

    function getInitialMenuState() {
        if (path.includes("/pages/games/forza/")) return MENU_STATES.FORZA;
        if (path.includes("/pages/games/ac/")) return MENU_STATES.AC;
        if (path.includes("/pages/games/pc/")) return MENU_STATES.PC;
        if (path.includes("/pages/games/")) return MENU_STATES.GAMES;
        return MENU_STATES.MAIN;
    }

    function abs(link) {
        return rootPrefix + link;
    }

    function normalizePathForMatch(inputPath) {
        if (!inputPath) return "";
        let normalized = inputPath.replace(/\/\/+$/, '');
        if (rootPrefix && normalized.startsWith(rootPrefix)) {
            normalized = normalized.slice(rootPrefix.length);
        }
        return normalized || "/";
    }

    function highlightMainNav() {
        const links = mainNav.querySelectorAll(".nav-link");
        const currentPath = path.toLowerCase();

        links.forEach(link => {
            link.classList.remove("active");
        });

        const activeLinkSelector = (keyword) => {
            return [...links].find(link => {
                const href = link.getAttribute("href") || "";
                const normalizedHref = normalizePathForMatch(href).toLowerCase();
                const normalizedText = link.textContent.trim().toLowerCase();

                if (normalizedHref.includes(keyword) || normalizedText === keyword) {
                    return true;
                }
                return false;
            });
        };

        let activeLink = null;

        if (currentPath.includes("/pages/main")) {
            activeLink = activeLinkSelector("/pages/main");
        } else if (currentPath.includes("/pages/about")) {
            activeLink = activeLinkSelector("/pages/about");
        } else if (currentPath.includes("/pages/stream")) {
            activeLink = activeLinkSelector("/pages/stream");
        } else if (currentPath.includes("/pages/team")) {
            activeLink = activeLinkSelector("/pages/team");
        } else if (currentPath.includes("/pages/partners")) {
            activeLink = activeLinkSelector("/pages/partners");
        } else if (currentPath.includes("/pages/games")) {
            const gamesLink = activeLinkSelector("игры");
            if (gamesLink) {
                activeLink = gamesLink;
            }
        }

        if (activeLink) {
            activeLink.classList.add("active");
        }
    }

    // ========================================================
    // ГЕНЕРАЦИЯ МЕНЮ - каждое меню возвращает HTML
    // ========================================================

    function getMainMenuHTML() {
        return `
            <a href="${abs('/pages/main/')}" class="nav-link">Главная</a>
            <a href="${abs('/pages/about/')}" class="nav-link">Обо мне</a>
            <a href="#" class="nav-link" data-menu-action="open-games">Игры</a>
            <a href="${abs('/pages/stream/')}" class="nav-link">Стрим</a>
            <a href="${abs('/pages/team/')}" class="nav-link">Команда</a>
            <a href="${abs('/pages/partners/')}" class="nav-link">Партнеры</a>
        `;
    }

    function getGamesMenuHTML() {
        return `
            <a href="#" class="nav-link back-link" data-menu-action="back">← Назад</a>
            <a href="#" class="nav-link game-series" data-menu-action="open-forza">Forza Motorsport</a>
            <a href="#" class="nav-link game-series" data-menu-action="open-ac">Assetto Corsa</a>
            <a href="#" class="nav-link game-series" data-menu-action="open-pc">Project Cars</a>
        `;
    }

    function getForzaMenuHTML() {
        return `
            <a href="#" class="nav-link back-link" data-menu-action="back">← Назад к сериям</a>
            <a href="${abs('/pages/games/forza/motorsport7/')}" class="nav-link">Forza Motorsport 7</a>
            <a href="${abs('/pages/games/forza/motorsport8/')}" class="nav-link">Forza Motorsport 8</a>
        `;
    }

    function getAcMenuHTML() {
        return `
            <a href="#" class="nav-link back-link" data-menu-action="back">← Назад к сериям</a>
            <a href="${abs('/pages/games/ac/carrera.html')}" class="nav-link">Assetto Corsa</a>
            <a href="${abs('/pages/games/ac/competizione.html')}" class="nav-link">Assetto Corsa Competizione</a>
        `;
    }

    function getPcMenuHTML() {
        return `
            <a href="#" class="nav-link back-link" data-menu-action="back">← Назад к сериям</a>
            <a href="${abs('/pages/games/pc/1.html')}" class="nav-link">Project Cars 1</a>
            <a href="${abs('/pages/games/pc/2.html')}" class="nav-link">Project Cars 2</a>
            <a href="${abs('/pages/games/pc/3.html')}" class="nav-link">Project Cars 3</a>
        `;
    }

    // ========================================================
    // УПРАВЛЕНИЕ МЕНЮ - переключение и обновление
    // ========================================================

    function getMenuHTML(state) {
        switch(state) {
            case MENU_STATES.GAMES: return getGamesMenuHTML();
            case MENU_STATES.FORZA: return getForzaMenuHTML();
            case MENU_STATES.AC: return getAcMenuHTML();
            case MENU_STATES.PC: return getPcMenuHTML();
            case MENU_STATES.MAIN:
            default: return getMainMenuHTML();
        }
    }

    function getMenuTitle(state) {
        switch(state) {
            case MENU_STATES.GAMES: return "Игры • СайтСотика";
            case MENU_STATES.FORZA: return "Forza Motorsport • СайтСотика";
            case MENU_STATES.AC: return "Assetto Corsa • СайтСотика";
            case MENU_STATES.PC: return "Project Cars • СайтСотика";
            case MENU_STATES.MAIN:
            default: return "СайтСотика";
        }
    }

    function setActiveInSubmenu(state) {
        const links = mainNav.querySelectorAll(".nav-link");
        links.forEach(link => link.classList.remove("active"));

        if (state === MENU_STATES.FORZA) {
            if (path.includes("/pages/games/forza/motorsport8")) {
                const activeLink = mainNav.querySelector("a[href*='motorsport8']");
                activeLink?.classList.add("active");
            } else if (path.includes("/pages/games/forza/motorsport7")) {
                const activeLink = mainNav.querySelector("a[href*='motorsport7']");
                activeLink?.classList.add("active");
            }
        } else if (state === MENU_STATES.AC) {
            if (path.includes("/pages/games/ac/carrera")) {
                const activeLink = mainNav.querySelector("a[href*='carrera']");
                activeLink?.classList.add("active");
            } else if (path.includes("/pages/games/ac/competizione")) {
                const activeLink = mainNav.querySelector("a[href*='competizione']");
                activeLink?.classList.add("active");
            }
        } else if (state === MENU_STATES.PC) {
            if (path.includes("/pages/games/pc/1.html")) {
                const activeLink = mainNav.querySelector("a[href*='/pages/games/pc/1.html']");
                activeLink?.classList.add("active");
            }
            if (path.includes("/pages/games/pc/2.html")) {
                const activeLink = mainNav.querySelector("a[href*='/pages/games/pc/2.html']");
                activeLink?.classList.add("active");
            }
            if (path.includes("/pages/games/pc/3.html")) {
                const activeLink = mainNav.querySelector("a[href*='/pages/games/pc/3.html']");
                activeLink?.classList.add("active");
            }
        } else if (state === MENU_STATES.GAMES) {
            // Если текущая страница находится в games, подсвечиваем пункт "Игры"
            const mainLinks = document.querySelectorAll('#main-nav .nav-link');
            mainLinks.forEach(l => l.classList.remove('active'));
            const gamesMainLink = [...mainLinks].find(l => l.textContent.trim().toLowerCase() === 'игры');
            gamesMainLink?.classList.add('active');
        }
    }

    function renderMenu(state) {
        // Обновляем содержимое основного меню
        mainNav.innerHTML = getMenuHTML(state);
        logo.textContent = getMenuTitle(state);

        if (state === MENU_STATES.MAIN) {
            highlightMainNav();
        } else {
            setActiveInSubmenu(state);
        }

        // Переподключаем обработчики событий
        attachEventListeners();
    }

    function openMenu(newState) {
        // Сохраняем текущее состояние в стек (для кнопки "Назад")
        menuStack.push(getCurrentMenuState());

        // Рендерим новое меню
        renderMenu(newState);
    }

    function goBack() {
        if (menuStack.length > 0) {
            const previousState = menuStack.pop();
            renderMenu(previousState);
        } else {
            // Если стек пуст, возвращаемся в главное меню
            renderMenu(MENU_STATES.MAIN);
        }
    }

    function getCurrentMenuState() {
        // Проверяем текущее содержимое mainNav чтобы вернуть его состояние
        const content = mainNav.innerHTML;

        if (content.includes("Forza Motorsport 7")) return MENU_STATES.FORZA;
        if (content.includes("Assetto Corsa Competizione")) return MENU_STATES.AC;
        if (content.includes("Project Cars 1")) return MENU_STATES.PC;
        if (content.includes("Forza Motorsport") && !content.includes("Forza Motorsport 7")) return MENU_STATES.GAMES;

        return MENU_STATES.MAIN;
    }

    // ========================================================
    // ОБРАБОТЧИКИ СОБЫТИЙ
    // ========================================================

    function attachEventListeners() {
        // Делегирование событий на mainNav
        mainNav.querySelectorAll("[data-menu-action]").forEach(element => {
            element.addEventListener("click", function(e) {
                const action = this.getAttribute("data-menu-action");

                if (action === "open-games") {
                    e.preventDefault();
                    openMenu(MENU_STATES.GAMES);
                } else if (action === "open-forza") {
                    e.preventDefault();
                    openMenu(MENU_STATES.FORZA);
                } else if (action === "open-ac") {
                    e.preventDefault();
                    openMenu(MENU_STATES.AC);
                } else if (action === "open-pc") {
                    e.preventDefault();
                    openMenu(MENU_STATES.PC);
                } else if (action === "back") {
                    e.preventDefault();
                    goBack();
                }
            });
        });
    }

    // ========================================================
    // МОБИЛЬНОЕ МЕНЮ
    // ========================================================

    const mobileBtn = document.createElement("button");
    mobileBtn.id = "mobile-menu-btn";
    mobileBtn.className = "mobile-menu-btn";
    mobileBtn.innerHTML = `
        <span class="hamburger-line"></span>
        <span class="hamburger-line"></span>
        <span class="hamburger-line"></span>
    `;
    header.appendChild(mobileBtn);

    // Мобильное меню - стек состояний
    const mobileMenuStack = [];
    let currentMobileState = MENU_STATES.MAIN;

    function renderMobileMenu(state) {
        currentMobileState = state;
        let html = ``;

        switch(state) {
            case MENU_STATES.GAMES:
                html = `
                    <a href="#" data-mobile-action="back">← Назад</a>
                    <a href="#" data-mobile-action="open-forza">Forza Motorsport</a>
                    <a href="#" data-mobile-action="open-ac">Assetto Corsa</a>
                    <a href="#" data-mobile-action="open-pc">Project Cars</a>
                `;
                break;
            case MENU_STATES.FORZA:
                html = `
                    <a href="#" data-mobile-action="back">← Назад</a>
                    <a href="/pages/games/forza/motorsport7/">Forza Motorsport 7</a>
                    <a href="/pages/games/forza/motorsport8/">Forza Motorsport 8</a>
                `;
                break;
            case MENU_STATES.AC:
                html = `
                    <a href="#" data-mobile-action="back">← Назад</a>
                    <a href="/pages/games/ac/carrera.html">Assetto Corsa</a>
                    <a href="/pages/games/ac/competizione.html">Assetto Corsa Competizione</a>
                `;
                break;
            case MENU_STATES.PC:
                html = `
                    <a href="#" data-mobile-action="back">← Назад</a>
                    <a href="/pages/games/pc/1.html">Project Cars 1</a>
                    <a href="/pages/games/pc/2.html">Project Cars 2</a>
                    <a href="/pages/games/pc/3.html">Project Cars 3</a>
                `;
                break;
            case MENU_STATES.MAIN:
            default:
                html = `
                    <a href="${abs('/pages/main/')}">Главная</a>
                    <a href="${abs('/pages/about/')}">Обо мне</a>
                    <a href="#" data-mobile-action="open-games">Игры</a>
                    <a href="${abs('/pages/stream/')}">Стрим</a>
                    <a href="${abs('/pages/team/')}">Команда</a>
                    <a href="${abs('/pages/partners/')}">Партнеры</a>
                `;
        }

        mobilePanel.innerHTML = html;
        attachMobileEventListeners();
    }

    function attachMobileEventListeners() {
        mobilePanel.querySelectorAll("[data-mobile-action]").forEach(element => {
            element.addEventListener("click", function(e) {
                const action = this.getAttribute("data-mobile-action");

                if (action === "open-games") {
                    e.preventDefault();
                    mobileMenuStack.push(MENU_STATES.MAIN);
                    renderMobileMenu(MENU_STATES.GAMES);
                } else if (action === "open-forza") {
                    e.preventDefault();
                    mobileMenuStack.push(MENU_STATES.GAMES);
                    renderMobileMenu(MENU_STATES.FORZA);
                } else if (action === "open-ac") {
                    e.preventDefault();
                    mobileMenuStack.push(MENU_STATES.GAMES);
                    renderMobileMenu(MENU_STATES.AC);
                } else if (action === "open-pc") {
                    e.preventDefault();
                    mobileMenuStack.push(MENU_STATES.GAMES);
                    renderMobileMenu(MENU_STATES.PC);
                } else if (action === "back") {
                    e.preventDefault();
                    if (mobileMenuStack.length > 0) {
                        const previousState = mobileMenuStack.pop();
                        renderMobileMenu(previousState);
                    } else {
                        renderMobileMenu(MENU_STATES.MAIN);
                        closeMobileMenu();
                    }
                }
            });
        });

        mobilePanel.querySelectorAll("a:not([data-mobile-action])").forEach(element => {
            element.addEventListener("click", function() {
                closeMobileMenu();
            });
        });
    }

    mobileBtn.addEventListener("click", () => {
        if (mobilePanel.classList.contains("open")) {
            closeMobileMenu();
        } else {
            openMobileMenu();
        }
    });

    // Инициализируем мобильное меню
    renderMobileMenu(MENU_STATES.MAIN);

    // ========================================================
    // АДАПТИВНОСТЬ - показ/скрытие меню в зависимости от размера
    // ========================================================

    function closeMobileMenu() {
        mobilePanel.classList.remove("open");
        mobileBtn.classList.remove("open");
    }

    function openMobileMenu() {
        mobilePanel.classList.add("open");
        mobileBtn.classList.add("open");
    }

    function updateMenuDisplay() {
        if (window.innerWidth <= 720) {
            // Мобильный режим
            mobileBtn.style.display = "flex";
            mainNav.classList.add("nav-hidden");
            closeMobileMenu();
        } else {
            // Десктопный режим
            mobileBtn.style.display = "none";
            mainNav.classList.remove("nav-hidden");
            closeMobileMenu();
            mobileMenuStack.length = 0;
            renderMobileMenu(MENU_STATES.MAIN);
        }
    }

    updateMenuDisplay();
    window.addEventListener("resize", updateMenuDisplay);

    // ========================================================
    // АНИМАЦИЯ ГРАДИЕНТА
    // ========================================================

    header.addEventListener("mousemove", (e) => {
        const x = e.clientX;
        const max = window.innerWidth;
        const hue = Math.floor((x / max) * 360);
        header.style.background = `linear-gradient(to right, #f8f9fa, hsl(${hue}, 40%, 90%), #f8f9fa)`;
    });

    header.addEventListener("mouseleave", () => {
        header.style.background = "#f8f9fa";
    });

    // Если пользователь сразу попал на вложенную игровую страницу, восстановим входной путь
    const initialState = getInitialMenuState();
    if ([MENU_STATES.FORZA, MENU_STATES.AC, MENU_STATES.PC].includes(initialState)) {
        menuStack.push(MENU_STATES.GAMES);
    } else if (initialState === MENU_STATES.GAMES) {
        menuStack.push(MENU_STATES.MAIN);
    }

    // Инициализируем основное меню
    renderMenu(initialState);
});