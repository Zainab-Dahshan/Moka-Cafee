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

let order = [];
let total = 0;

function addToOrder(itemName, price) {
    order.push({ name: itemName, price: price });
    total += price;
    renderOrder();
}

function renderOrder() {
    const orderList = document.getElementById('orderItems');
    const totalPrice = document.getElementById('totalPrice');
    if (!orderList || !totalPrice) return;

    orderList.innerHTML = '';
    order.forEach((item, index) => {
        const li = document.createElement('li');
        li.textContent = `${item.name} - ${item.price} جنيه`;
        orderList.appendChild(li);
    });

    totalPrice.textContent = total;
}

function finishOrder() {
    alert(`تم إرسال الطلب! الإجمالي: ${total} جنيه`);
    order = [];
    total = 0;
    renderOrder();
}
