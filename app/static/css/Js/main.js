// Main JS File – Moka-Cafe

document.addEventListener('DOMContentLoaded', () => {
    console.log("Main.js Loaded Successfully");

    // Mobile Menu Toggle (لو عندك Navbar)
    const toggleBtn = document.querySelector('.menu-toggle');
    const navMenu = document.querySelector('.nav-menu');

    if (toggleBtn && navMenu) {
        toggleBtn.addEventListener('click', () => {
            navMenu.classList.toggle('active');
        });
    }

    // Toast Auto-Hide Fix
    const toasts = document.querySelectorAll('.toast');
    toasts.forEach(toast => {
        new bootstrap.Toast(toast);
    });
    // Admin dashboard JS
    console.log("Admin JS loaded");
});