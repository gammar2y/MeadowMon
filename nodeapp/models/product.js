const mongoose = require('mongoose');
const Schema = mongoose.Schema;

const productSchema = new Schema({
  id: { type: Number, required: true, unique: true },
  name: { type: String, required: true },
  price: { type: Number, required: true },
  set: { type: String, required: true },
  description: { type: String, required: true },
  card_type: { type: String, required: true },
  bodyType: { type: String, required: true },
  year: { type: Number, required: true },
  image_url: { type: String, required: true }
});

const Product = mongoose.model('Product', productSchema);

module.exports = Product;