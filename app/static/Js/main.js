// Main JS File – Moka-Cafe

document.addEventListener('DOMContentLoaded', () => {
    console.log("Main.js Loaded Successfully");

    // Mobile Menu Toggle
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
        if (bootstrap) {
            new bootstrap.Toast(toast);
        }
    });

    console.log("Admin JS loaded");

    // لو الصفحة بتاعة الأوردر مفتوحة، اعرض البيانات
    renderOrder();
});

// =============================
// CART SYSTEM (Front-end only)
// =============================
let order = JSON.parse(localStorage.getItem("cart")) || [];
let total = JSON.parse(localStorage.getItem("total")) || 0;

// Add item to cart
function addToOrder(itemName, price) {
    order.push({ name: itemName, price: price });
    total += price;

    saveCart();
    renderOrder();

    alert("تمت الإضافة للأوردر");
}

// Display items in order page
function renderOrder() {
    const orderList = document.getElementById('orderItems');
    const totalPrice = document.getElementById('totalPrice');

    if (!orderList || !totalPrice) return;

    orderList.innerHTML = '';

    order.forEach((item) => {
        const li = document.createElement('li');
        li.textContent = `${item.name} - ${item.price} جنيه`;
        orderList.appendChild(li);
    });

    totalPrice.textContent = total;
}

// Save current cart
function saveCart() {
    localStorage.setItem("cart", JSON.stringify(order));
    localStorage.setItem("total", JSON.stringify(total));
}

// Finish order
function finishOrder() {
    alert(`تم إرسال الطلب! الإجمالي: ${total} جنيه`);

    order = [];
    total = 0;
    saveCart();
    renderOrder();
}
