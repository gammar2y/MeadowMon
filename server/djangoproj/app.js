require('dotenv').config({ path: './.env' });
const express = require('express');
const connectToDatabase = require('./database/db');

const app = express();

connectToDatabase().then(db => {
  // Use the `db` object to perform database operations
  app.get('/', async (req, res) => {
    const collection = db.collection('your-collection');
    const data = await collection.find({}).toArray();
    res.json(data);
  });

  const PORT = process.env.PORT || 3000;
  app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
  });
});