document.addEventListener("DOMContentLoaded", function () {
    const header = document.getElementById("main-header");
    const mainNav = document.getElementById("main-nav");
    const logo = header.querySelector(".logo");
    const links = header.querySelectorAll(".nav-link");
    const mobilePanel = document.getElementById("mobile-panel");

    // Определяем текущую страницу
    const path = window.location.pathname;
    const currentPage = path.split("/").pop() || "index.html";

    // Подсветка активной ссылки — через класс, а не инлайн-стили
    links.forEach(link => {
        if (link.getAttribute("href") === currentPage) {
            link.classList.add("active");
        }
    });

    // Очистка дополнительных меню
    function cleanup() {
        header.querySelectorAll("nav[id]:not(#main-nav)").forEach(nav => nav.remove());
    }

    // Стилизация навигации — убраны инлайны, оставляем CSS
    function styleNav(nav) {
        nav.style.display = "flex";
        nav.style.gap = "4px";
        nav.style.height = "100%";
        nav.style.alignItems = "center";
        nav.style.marginRight = "12px";
    }

    // Создание подменю "Игры"
    function createGamesNav() {
        cleanup();
        const gamesNav = document.createElement("nav");
        gamesNav.id = "games-nav";
        gamesNav.innerHTML = `
            <a href="#" class="nav-link back-link" data-back>← Назад</a>
            <a href="#" class="nav-link game-series" data-series="forza">Forza Motorsport</a>
            <a href="#" class="nav-link game-series" data-series="ac">Assetto Corsa</a>
            <a href="#" class="nav-link game-series" data-series="pc">Project Cars</a>
        `;
        styleNav(gamesNav);
        header.appendChild(gamesNav);
        logo.textContent = "Игры • СайтСотика";
    }

    // Подменю Forza
    function createForzaNav() {
        cleanup();
        const forzaNav = document.createElement("nav");
        forzaNav.id = "forza-nav";
        forzaNav.innerHTML = `
            <a href="#" class="nav-link back-link" data-back>← Назад к сериям</a>
            <a href="../games/forza/motorsport7.html" class="nav-link">Forza Motorsport 7</a>
            <a href="../games/forza/motorsport8.html" class="nav-link">Forza Motorsport 8</a>
        `;
        styleNav(forzaNav);
        header.appendChild(forzaNav);
        logo.textContent = "Forza Motorsport • СайтСотика";
    }

    // Подменю Assetto Corsa
    function createAcNav() {
        cleanup();
        const acNav = document.createElement("nav");
        acNav.id = "ac-nav";
        acNav.innerHTML = `
            <a href="#" class="nav-link back-link" data-back>← Назад к сериям</a>
            <a href="../games/ac/carrera.html" class="nav-link">Assetto Corsa</a>
            <a href="../games/ac/competizione.html" class="nav-link">Assetto Corsa Competizione</a>
        `;
        styleNav(acNav);
        header.appendChild(acNav);
        logo.textContent = "Assetto Corsa • СайтСотика";
    }

    // Подменю Project Cars
    function createPcNav() {
        cleanup();
        const pcNav = document.createElement("nav");
        pcNav.id = "pc-nav";
        pcNav.innerHTML = `
            <a href="#" class="nav-link back-link" data-back>← Назад к сериям</a>
            <a href="../games/pc/1.html" class="nav-link">Project Cars 1</a>
            <a href="../games/pc/2.html" class="nav-link">Project Cars 2</a>
            <a href="../games/pc/3.html" class="nav-link">Project Cars 3</a>
        `;
        styleNav(pcNav);
        header.appendChild(pcNav);
        logo.textContent = "Project Cars • СайтСотика";
    }

    // Обработчик клика по "Игры"
    header.querySelector("[data-page='games']").addEventListener("click", function (e) {
        e.preventDefault();
        mainNav.style.display = "none";
        createGamesNav();
        attachEventListeners();
    });

    // Привязка обработчиков событий
    function attachEventListeners() {
        header.querySelectorAll("[data-back]").forEach(button => {
            button.addEventListener("click", function (e) {
                e.preventDefault();
                const parentId = this.closest("nav").id;

                cleanup();

                if (["forza-nav", "ac-nav", "pc-nav"].includes(parentId)) {
                    createGamesNav();
                } else if (parentId === "games-nav") {
                    mainNav.style.display = "flex";
                    logo.textContent = "СайтСотика";
                }
                attachEventListeners();
            });
        });

        header.querySelectorAll("[data-series]").forEach(link => {
            link.addEventListener("click", function (e) {
                e.preventDefault();
                const series = this.getAttribute("data-series");
                if (series === "forza") createForzaNav();
                if (series === "ac") createAcNav();
                if (series === "pc") createPcNav();
                attachEventListeners();
            });
        });
    }

    // УДАЛЕНЫ: инлайновые стили хедера — доверяем CSS
    // header.style.cssText = `...` — теперь задаётся из header.css

    // Анимация градиента при движении мыши — заменена на безопасную
    header.addEventListener("mousemove", (e) => {
        const x = e.clientX;
        const max = window.innerWidth;
        const hue = Math.floor((x / max) * 360);
        // Только background, без других свойств
        header.style.background = `linear-gradient(to right, #f8f9fa, hsl(${hue}, 40%, 90%), #f8f9fa)`;
    });

    header.addEventListener("mouseleave", () => {
        header.style.background = "#f8f9fa";
    });

    attachEventListeners();

    // Мобильная кнопка меню
    const mobileBtn = document.createElement("button");
    mobileBtn.id = "mobile-menu-btn";
    mobileBtn.innerHTML = "☰";
    mobileBtn.style.cssText = `
        position: absolute;
        right: 12px;
        top: 50%;
        transform: translateY(-50%);
        width: 42px;
        height: 42px;
        border-radius: 8px;
        border: none;
        background: #6a11cb;
        color: white;
        font-size: 22px;
        font-weight: 700;
        cursor: pointer;
        z-index: 2000;
        display: none;
    `;
    header.appendChild(mobileBtn);

    // Генерация мобильного меню
    function renderMainMobileMenu() {
        mobilePanel.innerHTML = `
            <a href="../index.html">Главная</a>
            <a href="../about/index.html">Обо мне</a>
            <a href="#" data-mobile="games">Игры</a>
            <a href="../stream/index.html">Стрим</a>
            <a href="../team/index.html">Команда</a>
            <a href="../partners/index.html">Партнеры</a>
        `;
    }
    renderMainMobileMenu();

    mobileBtn.addEventListener("click", () => {
        mobilePanel.classList.toggle("open");
    });

    mobilePanel.addEventListener("click", (e) => {
        const target = e.target;

        if (target.dataset.mobile === "games") {
            mobilePanel.innerHTML = `
                <a href="#" data-mobile="back">← Назад</a>
                <a href="#" data-series="forza">Forza Motorsport</a>
                <a href="#" data-series="ac">Assetto Corsa</a>
                <a href="#" data-series="pc">Project Cars</a>
            `;
        }

        if (target.dataset.mobile === "back") {
            renderMainMobileMenu();
        }

        if (target.dataset.series === "forza") {
            mobilePanel.innerHTML = `
                <a href="#" data-mobile="back">← Назад</a>
                <a href="../games/forza/motorsport7.html">Forza Motorsport 7</a>
                <a href="../games/forza/motorsport8.html">Forza Motorsport 8</a>
            `;
        }

        if (target.dataset.series === "ac") {
            mobilePanel.innerHTML = `
                <a href="#" data-mobile="back">← Назад</a>
                <a href="../games/ac/carrera.html">Assetto Corsa</a>
                <a href="../games/ac/competizione.html">Assetto Corsa Competizione</a>
            `;
        }

        if (target.dataset.series === "pc") {
            mobilePanel.innerHTML = `
                <a href="#" data-mobile="back">← Назад</a>
                <a href="../games/pc/1.html">Project Cars 1</a>
                <a href="../games/pc/2.html">Project Cars 2</a>
                <a href="../games/pc/3.html">Project Cars 3</a>
            `;
        }
    });

    // Показ мобильного меню на малых экранах
    if (window.innerWidth <= 720) {
        mobileBtn.style.display = "block";
        mobilePanel.classList.add("open");
    }

    window.addEventListener("resize", () => {
        if (window.innerWidth > 720) {
            mobileBtn.style.display = "none";
            mobilePanel.classList.remove("open");
        } else {
            mobileBtn.style.display = "block";
            mobilePanel.classList.add("open");
        }
    });
});