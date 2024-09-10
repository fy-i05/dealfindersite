function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    const mainContent = document.getElementById('main-content');
    //check current width to decide whether to open or close  sidebar
    
    if (window.innerWidth <= 480) {  //check if the device width is less than or equal to 480px (phone?)
        if (sidebar.style.width === '0px') {
            sidebar.style.width = '100px';  
            mainContent.style.marginLeft = '150px';  
        } else {
            sidebar.style.width = '0px';  //close
            mainContent.style.marginLeft = '0px';
        }
    } else {
        // For larger screens 
        sidebar.style.width = sidebar.style.width === '250px' ? '0px' : '250px';
        mainContent.style.marginLeft = sidebar.style.marginLeft === '250px' ? '0px' : '250px';
    }
}


function filterByCategory(categoryId) {
    const url = `/api/products_by_category/?category_id=${categoryId}`;
    fetch(url)
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok: ' + response.statusText);
        }
        return response.json();
    })
    .then(data => {
        const productsContainer = document.querySelector('.product-grid');
        productsContainer.innerHTML = '';  //Clear existing products

        if (data.products.length > 0) {
            //Loop through the products and add them to the grid
            data.products.forEach(product => {
                productsContainer.innerHTML += `
                    <div class="product">
                        <a href="${product.link}" target="_blank">
                            <img src="${product.image}" alt="${product.name}">
                            <p>${product.name}</p>
                        </a>
                    </div>
                `;
            });
        } else {
            productsContainer.innerHTML = '<p>No products found for this category.</p>';
        }
    })
    .catch(error => console.error('Error loading the products:', error));
}


document.addEventListener("DOMContentLoaded", function() {
    const productNames = document.querySelectorAll('.product-name');

    productNames.forEach(function(name) {
        let words = name.innerText.split(' ');
        if (words.length > 5) {
            name.innerText = words.slice(0, 5).join(' ') + '...';
        }
    });
});