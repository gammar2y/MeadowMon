const mongoose = require('mongoose');
const express = require('express');
const app = express();

// MongoDB connection settings
const mongoURI = 'mongodb://localhost:27017/meadowmon'; // Replace with your MongoDB URI

mongoose.connect(mongoURI, {
  useNewUrlParser: true,
  useUnifiedTopology: true,
  serverSelectionTimeoutMS: 100000, // Increase timeout to 5 seconds
});

const db = mongoose.connection;
db.on('error', console.error.bind(console, 'MongoDB connection error:'));
db.once('open', () => {
  console.log('Connected to MongoDB');
  
  // Import and use your controllers
  const { loadProducts } = require('./controllers/productController');
  loadProducts();
});

app.listen(3000, () => {
  console.log('Server is running on port 3000');
});