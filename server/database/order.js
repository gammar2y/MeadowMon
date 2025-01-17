const mongoose = require('mongoose');

const { Schema } = mongoose;

const orders = new Schema({
  id: {
    type: Number,
    required: true,
  },
  city: {
    type: String,
    required: true,
  },
  state: {
    type: String,
    required: true,
  },
  address: {
    type: String,
    required: true,
  },
  zip: {
    type: String,
    required: true,
  },
  full_name: {
    type: String,
    required: true,
  },
});

module.exports = mongoose.model('orders', orders);
