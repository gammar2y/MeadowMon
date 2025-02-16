const mongoose = require('mongoose');
const express = require('express');
const path = require('path');
const app = express();

// MongoDB connection settings
const mongoURI = process.env.MONGODB_URI || 'mongodb+srv://meadowmonbusiness:NXVwZOXBQChb01uj@meadowmon.zcf42.mongodb.net/MeadowMon?retryWrites=true&w=majority';

mongoose.connect(mongoURI, {
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

// Serve static files from the frontend directory
app.use(express.static(path.join(__dirname, 'frontend/public')));

app.listen(3000, () => {
  console.log('Server is running on port 3000');
});