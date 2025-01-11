/*jshint esversion: 8 */
const express = require('express');
const mongoose = require('mongoose');
const fs = require('fs');
const cors = require('cors');
const app = express();
const port = 3030;

app.use(cors());
app.use(require('body-parser').urlencoded({ extended: false }));

const product_data = JSON.parse(fs.readFileSync('product.json', 'utf8'));
const cards_data = JSON.parse(fs.readFileSync('cards.json', 'utf8'));

mongoose.connect('mongodb://mongo_db:27017/', { dbName: 'cardsDB' });

const Product = require('./product');
const Cards = require('./cards');

try {
  Product.deleteMany({}).then(() => {
    Product.insertMany(product_data.product);
  });
  Cards.deleteMany({}).then(() => {
    Cards.insertMany(cards_data.cards);
  });
} catch (error) {
  res.status(500).json({ error: 'Error fetching documents' });
}

// Express route to home
app.get('/', async (req, res) => {
  res.send('Welcome to the Mongoose API');
});

// Express route to fetch all reviews
app.get('/fetchProduct', async (req, res) => {
  try {
    const documents = await Product.find();
    res.json(documents);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching documents' });
  }
});


// Express route to fetch all dealerships
app.get('/fetchCards', async (req, res) => {
  try {
    const documents = await Cards.find();
    res.json(documents);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching documents' });
  }
});

// Express route to fetch Dealers by a particular state
app.get('/fetchProduct/:set', async (req, res) => {
  try {
    const documents = await Product.find({ set: req.params.set });
    res.json(documents);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching documents' });
  }
});

// Express route to fetch dealer by a particular id
app.get('/fetchProduct/:id', async (req, res) => {
  try {
    const documents = await Product.find({ id: req.params.id });
    res.json(documents);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching documents' });
  }
});

// Express route to insert review
async function uploadOrder(order) {
  try {
    const response = await fetch('https://example.com/api/orders', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(order)
    });

    if (!response.ok) {
      throw new Error(`Error: ${response.statusText}`);
    }

 const orderData = {
  customerName: "John Doe",
  orderNumber: "12345",
  items: [
    { productId: "001", quantity: 2 },
    { productId: "002", quantity: 1 }
  ],
  totalAmount: 59.99
};

uploadOrder(orderData);

// Start the Express server
app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
} catch (error) {
  console.error('Failed to upload order:', error);
  // Additional error handling logic can be added here
}}