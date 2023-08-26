const mongoose = require('mongoose');

const { Schema } = mongoose;

const OrdersSchema = new Schema({
    userEmail: {
        type: String,
        required: true,
        unique: true,
    },
    orderData: {
        type: Array,
        required: true,
    },
});

module.exports = mongoose.model('Orders', OrdersSchema);
