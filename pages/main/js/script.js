document.addEventListener("DOMContentLoaded", function () {
    const header = document.getElementById("main-header");
    const mainNav = document.getElementById("main-nav");
    const logo = header.querySelector(".logo");
    const links = header.querySelectorAll(".nav-link");
    const mobilePanel = document.getElementById("mobile-panel");

    const path = window.location.pathname;
    const currentPage = path.split("/").pop() || "index.html";

    links.forEach(link => {
        if (link.getAttribute("href") === currentPage) {
            link.style.background = "#6a11cb";
            link.style.color = "white";
            link.style.fontWeight = "600";
        }
    });

    function cleanup() {
        header.querySelectorAll("nav[id]:not(#main-nav)").forEach(nav => nav.remove());
    }

    function styleNav(nav) {
        nav.style.cssText = `
            display: flex;
            gap: 4px;
            height: 100%;
            align-items: center;
            margin-right: 12px;
        `;
    }

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

    function createForzaNav() {
        cleanup();
        const forzaNav = document.createElement("nav");
        forzaNav.id = "forza-nav";
        forzaNav.innerHTML = `
            <a href="#" class="nav-link back-link" data-back>← Назад к сериям</a>
            <a href="games/forza/motorsport7.html" class="nav-link">Forza Motorsport 7</a>
            <a href="games/forza/motorsport8.html" class="nav-link">Forza Motorsport 8</a>
        `;
        styleNav(forzaNav);
        header.appendChild(forzaNav);
        logo.textContent = "Forza Motorsport • СайтСотика";
    }

    function createAcNav() {
        cleanup();
        const acNav = document.createElement("nav");
        acNav.id = "ac-nav";
        acNav.innerHTML = `
            <a href="#" class="nav-link back-link" data-back>← Назад к сериям</a>
            <a href="games/ac/carrera.html" class="nav-link">Assetto Corsa</a>
            <a href="games/ac/competizione.html" class="nav-link">Assetto Corsa Competizione</a>
        `;
        styleNav(acNav);
        header.appendChild(acNav);
        logo.textContent = "Assetto Corsa • СайтСотика";
    }

    function createPcNav() {
        cleanup();
        const pcNav = document.createElement("nav");
        pcNav.id = "pc-nav";
        pcNav.innerHTML = `
            <a href="#" class="nav-link back-link" data-back>← Назад к сериям</a>
            <a href="games/pc/1.html" class="nav-link">Project Cars 1</a>
            <a href="games/pc/2.html" class="nav-link">Project Cars 2</a>
            <a href="games/pc/3.html" class="nav-link">Project Cars 3</a>
        `;
        styleNav(pcNav);
        header.appendChild(pcNav);
        logo.textContent = "Project Cars • СайтСотика";
    }

    header.querySelector("[data-page='games']").addEventListener("click", function (e) {
        e.preventDefault();
        mainNav.style.display = "none";
        createGamesNav();
        attachEventListeners();
    });

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

    header.style.cssText = `
        width: 100%;
        height: 60px;
        background: #f8f9fa;
        border-bottom: 1px solid #dee2e6;
        position: fixed;
        top: 0;
        left: 0;
        z-index: 1000;
        font-family: 'Segoe UI', sans-serif;
        overflow: hidden;
        padding: 0;
        margin: 0;
        display: flex;
        align-items: center;
        justify-content: space-between;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    `;

    logo.style.cssText = `
        color: #6a11cb;
        font-size: 1.1em;
        font-weight: 700;
        margin-left: 16px;
        letter-spacing: 0.5px;
        white-space: nowrap;
        transition: all 0.3s ease;
    `;

    styleNav(mainNav);

    header.addEventListener("mousemove", (e) => {
        const x = e.clientX;
        const max = window.innerWidth;
        const hue = Math.floor((x / max) * 360);
        header.style.background = `linear-gradient(to right, #f8f9fa, hsl(${hue}, 40%, 90%), #f8f9fa)`;
    });

    header.addEventListener("mouseleave", () => {
        header.style.background = "#f8f9fa";
    });

    attachEventListeners();

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

    function renderMainMobileMenu() {
        mobilePanel.innerHTML = `
            <a href="index.html">Главная</a>
            <a href="about.html">Обо мне</a>
            <a href="#" data-mobile="games">Игры</a>
            <a href="stream.html">Стрим</a>
            <a href="team.html">Команда</a>
            <a href="partners.html">Партнеры</a>
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
                <a href="games/forza/motorsport7.html">Forza Motorsport 7</a>
                <a href="games/forza/motorsport8.html">Forza Motorsport 8</a>
            `;
        }

        if (target.dataset.series === "ac") {
            mobilePanel.innerHTML = `
                <a href="#" data-mobile="back">← Назад</a>
                <a href="games/ac/carrera.html">Assetto Corsa</a>
                <a href="games/ac/competizione.html">Assetto Corsa Competizione</a>
            `;
        }

        if (target.dataset.series === "pc") {
            mobilePanel.innerHTML = `
                <a href="#" data-mobile="back">← Назад</a>
                <a href="games/pc/1.html">Project Cars 1</a>
                <a href="games/pc/2.html">Project Cars 2</a>
                <a href="games/pc/3.html">Project Cars 3</a>
            `;
        }
    });

    window.addEventListener("resize", () => {
        if (window.innerWidth > 720) {
            mobilePanel.classList.remove("open");
        }
    });
});
