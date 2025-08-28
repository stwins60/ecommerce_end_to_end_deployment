// Modern E-commerce Cart JS
async function addToCart(id) {
    const res = await fetch("/cart", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({id})
    });
    const cart = await res.json();
    updateCart(cart);
}


function updateCart(cart) {
    const cartList = document.getElementById("cart-list");
    cartList.innerHTML = cart.map(item => `<li>${item.name} - $${item.price} <button onclick="removeFromCart(${item.id})" style="margin-left:10px;color:#fff;background:#d9534f;border:none;border-radius:3px;padding:2px 8px;cursor:pointer;">Remove</button></li>`).join("");
    document.getElementById("cart-count").textContent = cart.length;
}

async function removeFromCart(id) {
    // Remove a single item from cart
    const res = await fetch("/cart", {
        method: "DELETE",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({id})
    });
    const cart = await res.json();
    updateCart(cart);
}

window.onload = async function() {
    const res = await fetch("/cart");
    const cart = await res.json();
    updateCart(cart);
        // Enable checkout navigation if cart has items
        const checkoutBtn = document.getElementById("checkout-btn");
        if (checkoutBtn) {
            checkoutBtn.disabled = cart.length === 0;
            checkoutBtn.onclick = function() {
                if (cart.length > 0) window.location.href = "/checkout";
            };
        }
    };
