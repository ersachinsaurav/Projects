const express = require('express');
const router = express.Router();
const Orders = require('../models/Orders');

router.post('/placeOrder', async (req, res) => {
    const newOrderData = req.body.orderData;
    await newOrderData.splice(0, 0, { orderDate: req.body.orderDate });

    const userExistingOrders = await Orders.findOne({ userEmail: req.body.email });
    if (userExistingOrders === null) {
        try {
            await Orders.create({
                userEmail: req.body.email,
                orderData: [newOrderData],
            }).then(() => {
                res.json({ success: true });
            });
        } catch (error) {
            console.log(error.message);
            res.send('Server Error', error.message);
        }
    } else {
        try {
            await Orders.findOneAndUpdate({ userEmail: req.body.email }, { $push: { orderData: newOrderData } }).then(() => {
                res.json({ success: true });
            });
        } catch (error) {
            console.log(error.message);
            res.send('Server Error', error.message);
        }
    }
});

router.post('/getOrderData', async (req, res) => {
    try {
        const orderData = await Orders.findOne({ userEmail: req.body.email });
        res.json({ orderData });
    } catch (error) {
        res.send('Error', error.message);
    }
});

module.exports = router;
