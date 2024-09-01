document.addEventListener('DOMContentLoaded', () => {
    // Load products when the page is ready
    fetchProducts();

    // Handle form submission for orders
    document.querySelector('form[action="/"]').addEventListener('submit', handleOrderSubmit);

    // Handle reset button click
    document.querySelector('form[action="/reset"]').addEventListener('submit', handleResetSubmit);
});

// Function to fetch products from the backend API and display them on the page
function fetchProducts() {
    fetch('/api/products')
        .then(response => response.json())
        .then(data => {
            // Populate the products in the form
              const productContainer = document.getElementById('product-list');
            productContainer.innerHTML = '';

            data.forEach(product => {
                // Create a new product element with product details
                const productElement = document.createElement('div');
                productElement.className = 'flex items-center mb-2';
                productElement.innerHTML = `
                    <label for="produkt${product.ProduktId}" class="w-2/3 text-sm">${product.Name} (Verfügbar: ${product.VerfuegbareMenge})</label>
                    <select name="menge${product.ProduktId}" class="w-1/3 border rounded p-1">
                        ${Array.from({length: 11}, (_, i) => `<option value="${i}">${i}</option>`).join('')}
                    </select>
                `;
                productContainer.appendChild(productElement); //add product
            });
        })
        .catch(error => console.error('Error fetching products:', error));
}

// Function to handle form submission for placing an order
function handleOrderSubmit(event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const orders = [];

    // Iterate over form data to gather order details
    for (const [key, value] of formData.entries()) {
        if (key.startsWith('menge') && value) {
            const produktId = parseInt(key.replace('menge', ''));
            const menge = parseInt(value);
            if (menge > 0) {
                orders.push({ProduktId: produktId, Menge: menge});
            }
        }
    }

    if (orders.length > 0) {
        fetch('/api/order', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({orders}),
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message || data.error);
            if (data.message) {
                fetchProducts();
            }
        })
        .catch(error => console.error('Error placing order:', error));
    } else {
        alert('No valid orders found.');
    }
}

// Function to handle form submission for resetting inventory
function handleResetSubmit(event) {
    event.preventDefault();
    fetch('/api/reset', {
        method: 'POST',
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message || data.error);
        if (data.message) {
            fetchProducts(); // Refresh product list
        }
    })
    .catch(error => console.error('Error resetting inventory:', error));
}
