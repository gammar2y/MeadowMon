const { Int32 } = require('mongodb');
const mongoose = require('mongoose');

const { Schema } = mongoose;

const product = new Schema({
  product_id: {
    type: Number,
    required: true,
  },
  set: {
    type: String,
    required: true,
  },
  card_type: {
    type: String,
    required: true,
  },
  bodyType: {
    type: String,
    required: true,
  },
  year: {
    type: Number,
    required: true,
  },
  price: {
    type: Number,
    required: true,
  },
});

module.exports = mongoose.model('product', product);
