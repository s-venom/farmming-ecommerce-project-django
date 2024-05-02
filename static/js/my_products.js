
function openDeleteModal(productId, productCatg, productName, productDesc, productPrice, productWQ, productDig, productStock) {
    // Retrieve product details using AJAX or from an array of products
    var product = getProductDetails(productId, productCatg, productName, productDesc, productPrice, productWQ, productDig, productStock);
    // Set the values of the delete modal form fields
    document.getElementById('deleteProductId').value = product.id;
    document.getElementById('deleteProductName').textContent = productName;

    var deleteModal = new bootstrap.Modal(document.getElementById('deleteProductModal'));
    deleteModal.show();
}

function openEditModal(productId, productCatg, productName, productDesc, productPrice, productWQ, productDig, productStock) {
    // Retrieve product details using AJAX or from an array of products
    var product = getProductDetails(productId, productCatg, productName, productDesc, productPrice, productWQ, productDig, productStock);
    // Set the values of the edit modal form fields
    document.getElementById('editProductId').value = product.id;
    //document.getElementById('editCategories').value = product.category_id;
    document.getElementById('editProductName').value = product.name;
    document.getElementById('editDescription').value = product.description;
    document.getElementById('editPrice').value = product.price;
    document.getElementById('editWeightQuantity').value = product.weight_quantity;
    document.getElementById('editDigital').checked = product.digital;
    document.getElementById('editStock').value = product.stock;
    
    // Set the selected category
    var categorySelect = document.getElementById('editCategories');
    for (var i = 0; i < categorySelect.options.length; i++) {
        if (categorySelect.options[i].value == productCatg) {
            categorySelect.selectedIndex = i;
            break;
        }
    }
    // Show the edit product modal
    var editProductModal = new bootstrap.Modal(document.getElementById('editProductModal'));
    editProductModal.show();
}

function getProductDetails(productId, productCatg, productName, productDesc, productPrice, productWQ, productDig, productStock) {
    // Replace this with actual code to fetch product details using AJAX or from an array of products
    return {
        id: productId,
        name: productName,
        description: productDesc,
        price: productPrice,
        weight_quantity: productWQ,
        digital: productDig,
        stock: productStock
    };
}