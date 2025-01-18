require('dotenv').config();
const { MongoClient } = require('mongodb');

const uri = process.env.MONGODB_URI;
const client = new MongoClient(uri, { useNewUrlParser: true, useUnifiedTopology: true });

async function connectToDatabase() {
  try {
    await client.connect();
    console.log("Connected to MongoDB Atlas");
    return client.db('<dbname>'); // Replace <dbname> with your database name
  } catch (err) {
    console.error(err);
    process.exit(1);
  }
}

module.exports = connectToDatabase;