const mongoose = require('mongoose');
const Schema = mongoose.Schema;

const cardModelSchema = new Schema({
  card: { type: mongoose.Schema.Types.ObjectId, ref: 'Product', required: true },
  name: { type: String, required: true },
  type: { type: String, enum: ['Graded', 'Singles', 'Boxes'], default: 'PACK', required: true }
});

const CardModel = mongoose.model('CardModel', cardModelSchema);

module.exports = CardModel;