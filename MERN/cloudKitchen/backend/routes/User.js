const express = require('express');
const router = express.Router();
const Users = require('../models/Users');
const { body, validationResult } = require('express-validator');
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
const jwtSecret = 'FalanaDhimkana';

router.post(
    '/createUser',
    body('name', 'Name must be of minimum 3 characters.').isLength({ min: 3 }),
    body('location', 'Location must be of minimum 3 characters.').isLength({
        min: 3,
    }),
    body('email', 'Email must be in valid format.').isEmail(),
    body('password', 'Password must be of minimum 5 characters.').isLength({
        min: 5,
    }),
    async (req, res) => {
        const errors = validationResult(req);
        if (!errors.isEmpty()) {
            return res.status(400).json({ errors: errors.array() });
        }

        const salt = await bcrypt.genSalt(10);
        const password = await bcrypt.hash(req.body.password, salt);

        try {
            await Users.create({
                name: req.body.name,
                email: req.body.email,
                location: req.body.location,
                password: password,
            });
            res.json({ success: true, message: 'User created successfully' });
        } catch (error) {
            console.log(error);
            res.json({ success: false, message: error.message });
        }
    }
);

router.post(
    '/authUser',
    body('email', 'Email must be in valid format.').isEmail(),
    body('password', 'Password must be of minimum 5 characters.').isLength({
        min: 5,
    }),
    async (req, res) => {
        const errors = validationResult(req);
        if (!errors.isEmpty()) {
            return res.status(400).json({ errors: errors.array() });
        }

        try {
            const { email, password } = req.body;
            const userData = await Users.findOne({ email });

            if (!userData) {
                return res.status(400).json({ success: false, message: 'Invalid Email' });
            }

            const isCorrectPassword = await bcrypt.compare(password, userData.password);

            if (!isCorrectPassword) {
                return res.status(400).json({ success: false, message: 'Invalid Credentials' });
            }

            const fetchedUserData = { user: { id: userData.id } };
            const authToken = jwt.sign(fetchedUserData, jwtSecret);

            res.json({ success: true, authToken });
        } catch (error) {
            console.log(error);
            res.json({ success: false, message: error.message });
        }
    }
);

module.exports = router;
