const express = require("express");
const User = require("../models/User");
const router = express.Router();
const { body, validationResult } = require("express-validator");
const bcrypt = require("bcryptjs");
const jwt = require("jsonwebtoken");
const JWT_SECRET = "IamBEST";
const fetchuser = require("../middleware/fetchuser");

// Create a User using POST "/api/auth/createuser".
router.post(
  "/createuser",
  [
    body("name", "Name should be minimum of three characters.").isLength({
      min: 3,
    }),
    body("email", "Valid Email is required.").isEmail(),
    body("password", "Password should be minimum of six characters.").isLength({
      min: 6,
    }),
  ],
  async (req, res) => {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({ status: false, message: errors.array() });
    }

    try {
      // validating email
      let user = await User.findOne({ email: req.body.email });
      if (user) {
        return res
          .status(400)
          .json({ status: false, message: "Email already exists." });
      }

      const salt = await bcrypt.genSalt(10);
      const hashedPassword = await bcrypt.hash(req.body.password, salt);

      // posting data to database after validation
      user = await User.create({
        name: req.body.name,
        password: hashedPassword,
        email: req.body.email,
      });

      const data = {
        user: {
          id: user.id,
        },
      };

      const responseData = {
        status: true,
        authToken: jwt.sign(data, JWT_SECRET),
        message: "User created successfully.",
      };
      res.status(200).json(responseData);
    } catch (error) {
      console.log(error.message);
      return res
        .status(500)
        .json({ status: false, message: "Internal Server Error" });
    }
  }
);

// Login using POST "/api/auth/login".
router.post(
  "/login",
  [
    body("email", "Valid Email is required.").isEmail(),
    body("password", "Password is required.").exists(),
  ],
  async (req, res) => {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({ status: false, message: errors.array() });
    }

    const { email, password } = req.body;
    try {
      let user = await User.findOne({ email });

      if (!user) {
        return res
          .status(400)
          .json({ status: false, message: "Invalid credentials." });
      }

      const correctPassword = await bcrypt.compare(password, user.password);
      if (!correctPassword) {
        return res
          .status(400)
          .json({ status: false, message: "Invalid credentials." });
      }

      const data = {
        user: {
          id: user.id,
        },
      };

      const responseData = {
        status: true,
        authToken: jwt.sign(data, JWT_SECRET),
        message: "User authenticated successfully.",
      };

      res.json(responseData);
    } catch (error) {
      console.log(error.message);
      return res
        .status(500)
        .json({ status: false, message: "Internal Server Error" });
    }
  }
);

// Fetch logged in user data using POST "api/auth/getuser" | Login Required
router.post("/getuser", fetchuser, async (req, res) => {
  try {
    let userId = req.user.id;
    const user = await User.findById(userId).select("-password");
    res.json({ status: true, user });
  } catch (error) {
    console.log(error.message);
    return res
      .status(500)
      .json({ status: false, message: "Internal Server Error" });
  }
});

module.exports = router;
