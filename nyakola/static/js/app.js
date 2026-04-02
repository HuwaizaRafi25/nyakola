// ==== Admin Layout

// Notif JS
document.addEventListener("DOMContentLoaded", function () {
    const notifButton = document.getElementById("notifButton");
    const notifCard = document.getElementById("notif");
    const closeNotif = document.getElementById("closeNotif");

    notifButton.addEventListener("click", function () {
        notifCard.classList.remove("hidden");
        notifCard.classList.add("flex");
    });

    closeNotif.addEventListener("click", function () {
        notifCard.classList.add("hidden");
        notifCard.classList.remove("flex");
    });

    notifCard.addEventListener("click", function (e) {
        if (e.target === notifCard) {
            notifCard.classList.add("hidden");
            notifCard.classList.remove("flex");
        }
    });
});

// Sidebar JS
const navLinks = document.querySelectorAll(".nav-link");
const subNavLinks = document.querySelectorAll(".sub-nav-text");

const routes = {
    navLinks: {
        1: "/dashboard",
        2: "/attendances",
        3: "/announcement",
        4: "/job",
        // 5: "/documents",
        5: "/dues",
        6: "/application-settings",
        7: "/activity-logs",
    },
    subNavLinks: {
        1: "/users",
        2: "/roles-permissions",
        3: "/locations",
        4: "/help-center",
        5: "/contact-support",
    },
};

navLinks.forEach((navLink) => {
    navLink.addEventListener("click", (e) => {
        e.preventDefault();
        const navLinkId = navLink.getAttribute("data-navLink");
        const submenu = navLink.nextElementSibling;

        if (submenu && submenu.classList.contains("submenu")) {
            toggleSubmenu(submenu, navLink.querySelector(".bx-chevron-down"));
        } else {
            const route = routes.navLinks[navLinkId];
            if (route) {
                navigateToRoute(route);
            }
        }
    });
});

subNavLinks.forEach((subNavText) => {
    subNavText.addEventListener("click", (e) => {
        e.preventDefault();
        const subNavTextId = subNavText.getAttribute("data-subNavText");
        const route = routes.subNavLinks[subNavTextId];
        if (route) {
            navigateToRoute(route);
        }
    });
});

function toggleSubmenu(submenu, iconChevron) {
    const isActive = submenu.classList.contains("submenu-active");
    closeAllSubmenus();
    if (!isActive) {
        submenu.classList.add("submenu-active");
        submenu.style.maxHeight = submenu.scrollHeight + "px";
        iconChevron.classList.add("-rotate-90");
    }
}

function navigateToRoute(route) {
    if (route) {
        window.location.href = route;
    } else {
        console.error("Route not found");
    }
}

function setActiveState() {
    const currentPath = window.location.pathname;

    removeActiveClasses(navLinks);
    removeSubNavLinkActiveClasses(subNavLinks);
    closeAllSubmenus();

    for (const [id, route] of Object.entries(routes.navLinks)) {
        if (currentPath === route) {
            const navLink = document.querySelector(
                `.nav-link[data-navLink="${id}"]`
            );
            if (navLink) {
                navLink.classList.add("nav-link-active");
                const submenu = navLink.nextElementSibling;
                if (submenu && submenu.classList.contains("submenu")) {
                    openSubmenu(
                        submenu,
                        navLink.querySelector(".bx-chevron-down")
                    );
                }
            }
            break;
        }
    }

    for (const [id, route] of Object.entries(routes.subNavLinks)) {
        if (currentPath === route) {
            const subNavText = document.querySelector(
                `.sub-nav-text[data-subNavText="${id}"]`
            );
            if (subNavText) {
                subNavText.classList.add("sub-nav-text-active");
                const parentNavLink =
                    subNavText.closest(".submenu").previousElementSibling;
                if (parentNavLink) {
                    parentNavLink.classList.add("nav-link-active");
                    const submenu = parentNavLink.nextElementSibling;
                    const iconChevron =
                        parentNavLink.querySelector(".bx-chevron-down");
                    if (submenu && iconChevron) {
                        openSubmenu(submenu, iconChevron);
                    }
                }
            }
            break;
        }
    }
}

function openSubmenu(submenu, iconChevron) {
    submenu.classList.add("submenu-active");
    submenu.style.maxHeight = submenu.scrollHeight + "px";
    iconChevron.classList.add("-rotate-90");
}

function closeAllSubmenus() {
    const allSubmenus = document.querySelectorAll(".submenu-active");

    allSubmenus.forEach((submenu) => {
        submenu.classList.remove("submenu-active");
        submenu.style.maxHeight = null;

        const iconChevron =
            submenu.previousElementSibling.querySelector(".bx-chevron-down");
        if (iconChevron) {
            iconChevron.classList.remove("-rotate-90");
        }
    });
}

function removeActiveClasses(links) {
    links.forEach((link) => link.classList.remove("nav-link-active"));
}

function removeSubNavLinkActiveClasses(links) {
    links.forEach((link) => link.classList.remove("sub-nav-text-active"));
}
document.addEventListener("DOMContentLoaded", setActiveState);

function navigateTo(url) {
    document.querySelectorAll('.sub-nav-link').forEach(link => {
        link.classList.remove('active');
    });
    event.currentTarget.classList.add('active');
    window.location.href = url;
}

document.addEventListener('DOMContentLoaded', () => {
    const sidebar = document.querySelector('.sidebar');
    const sidebarLayer = document.getElementById('sidebarLayer');
    const toggle = document.querySelector('.toggle');
    const home = document.querySelector('.home');

    const updateSidebarState = () => {
        if (window.innerWidth >= 1024) {
            // Untuk layar lg ke atas - sidebar defaultnya terbuka
            sidebar.classList.remove('close');
            sidebar.classList.remove('-translate-x-full');
            sidebarLayer.classList.add('hidden');
            home.classList.add('lg:left-[296px]');
            home.style.width = 'calc(100% - 296px)';
        } else {
            // Untuk layar di bawah lg - sidebar defaultnya tertutup
            sidebar.classList.add('close');
            sidebar.classList.add('-translate-x-full');
            sidebarLayer.classList.add('hidden');
            home.classList.remove('lg:left-[296px]');
            home.style.width = '100%';
        }
    };

    const toggleSidebar = () => {
        if (window.innerWidth >= 1024) {
            // Toggle untuk layar lg ke atas
            if (!sidebar.classList.contains('close')) {
                // Jika sidebar terbuka, tutup sidebar
                sidebar.classList.add('close');
                sidebar.classList.add('-translate-x-full');
                home.style.width = '100%';
                home.classList.remove('lg:left-[296px]');
            } else {
                // Jika sidebar tertutup, buka sidebar
                sidebar.classList.remove('close');
                sidebar.classList.remove('-translate-x-full');
                home.style.width = 'calc(100% - 296px)';
                home.classList.add('lg:left-[296px]');
            }
        } else {
            // Toggle untuk layar di bawah lg
            if (sidebar.classList.contains('close')) {
                // Jika sidebar tertutup, buka sidebar (overlay)
                sidebar.classList.remove('close');
                sidebar.classList.remove('-translate-x-full');
                sidebarLayer.classList.remove('hidden');
            } else {
                // Jika sidebar terbuka, tutup sidebar
                sidebar.classList.add('close');
                sidebar.classList.add('-translate-x-full');
                sidebarLayer.classList.add('hidden');
            }
        }
    };

    // Event listeners
    toggle.addEventListener('click', toggleSidebar);
    sidebarLayer.addEventListener('click', toggleSidebar);
    window.addEventListener('resize', updateSidebarState);

    // Inisialisasi
    updateSidebarState();
});
