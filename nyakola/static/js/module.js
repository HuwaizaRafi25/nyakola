const navLinks = document.querySelectorAll(".nav-link");
const subNavLinks = document.querySelectorAll(".sub-nav-link");

navLinks.forEach((navLink) => {
    navLink.addEventListener("click", () => {
        const submenu = navLink.nextElementSibling;

        if (submenu && submenu.classList.contains("submenu")) {
            toggleSubmenu(submenu, navLink.querySelector(".bx-chevron-down"));
        }
    });
});

function toggleSubmenu(submenu, iconChevron) {
    const isActive = submenu.classList.contains("submenu-active");
    closeAllSubmenus();

    if (!isActive) {
        submenu.classList.add("submenu-active");
        submenu.style.maxHeight = submenu.scrollHeight + "px";
        if (iconChevron) iconChevron.classList.add("-rotate-90");
    }
}

function closeAllSubmenus() {
    document.querySelectorAll(".submenu-active").forEach((submenu) => {
        submenu.classList.remove("submenu-active");
        submenu.style.maxHeight = null;

        const iconChevron =
            submenu.previousElementSibling.querySelector(".bx-chevron-down");
        if (iconChevron) {
            iconChevron.classList.remove("-rotate-90");
        }
    });
}

function setActiveState() {
    const currentPath = window.location.pathname;

    subNavLinks.forEach((link) => {
        const a = link.querySelector("a");

        if (a && a.getAttribute("href") === currentPath) {
            link.classList.add("active");

            const submenu = link.closest(".submenu");
            if (submenu) {
                submenu.classList.add("submenu-active");
                submenu.style.maxHeight = submenu.scrollHeight + "px";

                const parentNav = submenu.previousElementSibling;
                if (parentNav) {
                    parentNav.classList.add("nav-link-active");
                }
            }
        }
    });
}


document.addEventListener("DOMContentLoaded", setActiveState);


console.log("Module loaded successfully.");