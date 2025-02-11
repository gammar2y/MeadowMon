const mongoose = require('mongoose');
const fs = require('fs');
const path = require('path');
const Product = require('../models/product'); // Ensure this import is correct

const loadProducts = async () => {
  const jsonFilePath = path.join(__dirname, '../database/data/products.json');

  try {
    console.log(`Loading products from ${jsonFilePath}`);
    const data = fs.readFileSync(jsonFilePath, 'utf8');
    const products = JSON.parse(data).products;

    for (const productData of products) {
      const requiredFields = ['id', 'name', 'price', 'set', 'description', 'card_type', 'bodyType', 'year', 'image_url'];
      const missingFields = requiredFields.filter(field => !productData.hasOwnProperty(field));

      if (missingFields.length === 0) {
        console.log(`Product data before update: ${JSON.stringify(productData)}`);
        await Product.updateOne(
          { id: productData.id },
          productData,
          { upsert: true }
        );
        console.log(`Processed product: ${productData.id}`);
      } else {
        console.error(`Missing fields ${missingFields} in product data: ${JSON.stringify(productData)}`);
      }
    }
    console.log('Successfully loaded products');
  } catch (err) {
    console.error('Error loading products:', err);
  }
};

// Test MongoDB connection
mongoose.connect(process.env.MONGODB_URI, { useNewUrlParser: true, useUnifiedTopology: true })
  .then(() => {
    console.log('MongoDB connected successfully');
    loadProducts();
  })
  .catch(err => {
    console.error('MongoDB connection error:', err);
  });

module.exports = { loadProducts };