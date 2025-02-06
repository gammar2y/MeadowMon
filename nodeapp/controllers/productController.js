const Product = require('../models/product');
const fs = require('fs');
const path = require('path');

const loadProducts = async () => {
  const jsonFilePath = path.join(__dirname, '..', 'database', 'data', 'products.json');

  try {
    console.log(`Loading products from ${jsonFilePath}`);
    const data = fs.readFileSync(jsonFilePath, 'utf8');
    const products = JSON.parse(data).products;

    for (const productData of products) {
      const requiredFields = ['product_id', 'name', 'price', 'set', 'description', 'card_type', 'bodyType', 'year', 'image_url'];
      const missingFields = requiredFields.filter(field => !productData.hasOwnProperty(field));

      if (missingFields.length === 0) {
        await Product.updateOne(
          { product_id: productData.product_id },
          productData,
          { upsert: true }
        );
        console.log(`Processed product: ${productData.product_id}`);
      } else {
        console.error(`Missing fields ${missingFields} in product data: ${JSON.stringify(productData)}`);
      }
    }
    console.log('Successfully loaded products');
  } catch (err) {
    console.error('Error loading products:', err);
  }
};

// Call the function to load products
loadProducts();

module.exports = { loadProducts };