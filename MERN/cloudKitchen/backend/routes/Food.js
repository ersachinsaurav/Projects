const express = require('express');
const router = express.Router();

router.post('/foodItems', (req, res) => {
    try {
        res.send(global.foodItems);
    } catch (error) {
        console.log(error);
        return res.status(400).json({ errors: error.message });
    }
});

router.post('/foodCategories', (req, res) => {
    try {
        res.send(global.foodCategories);
    } catch (error) {
        console.log(error);
        return res.status(400).json({ errors: error.message });
    }
});

module.exports = router;
