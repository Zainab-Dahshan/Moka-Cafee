document.addEventListener('DOMContentLoaded', function() {
    const addToCartButtons = document.querySelectorAll('.add-to-cart');
    const cartCount = document.getElementById('cart-count');

    addToCartButtons.forEach(button => {
        button.addEventListener('click', function() {
            const itemId = this.getAttribute('data-id');

            fetch('/add_to_cart/' + itemId, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({})
            })
            .then(response => response.json())
            .then(data => {
                cartCount.textContent = data.cart_count;

                // Show success toast
                const toastEl = document.getElementById('addedToCartToast');
                if (toastEl) {
                    new bootstrap.Toast(toastEl).show();
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('هناك مشكلة في إضافة العنصر للأوردر. حاول مرة أخرى.');
            });
        });
    });

    // If order page, render cart items from session via API or backend
    renderOrderFromBackend();
});

// Optional: Render order page (this needs backend integration)
function renderOrderFromBackend() {
    const orderList = document.getElementById('orderItems');
    const totalPrice = document.getElementById('totalPrice');

    if (!orderList || !totalPrice) return;

    fetch('/get_cart') // You'll need to create this endpoint in your backend
        .then(res => res.json())
        .then(cart => {
            orderList.innerHTML = '';
            let total = 0;
            Object.values(cart).forEach(item => {
                const li = document.createElement('li');
                li.textContent = `${item.name} - ${item.price} جنيه × ${item.quantity}`;
                orderList.appendChild(li);
                total += parseFloat(item.price) * item.quantity;
            });
            totalPrice.textContent = total;
        });
}
