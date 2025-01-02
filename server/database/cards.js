const mongoose = require('mongoose');

const { Schema } = mongoose;

const reviews = new Schema({
  id: {
    type: Number,
    required: true,
  },
  name: {
    type: String,
    required: true,
  },
  year: {
    type: Number,
    required: true,
  },
  set: {
    type: String,
    required: true,
  },
  quantity: {
    type: Number,
    required: true,
  },
  grade: {
    type: Number,
    required: true,
  },
  price: {
    type: Number,
    required: true,
  },
});

module.exports = mongoose.model('cards', cards);
