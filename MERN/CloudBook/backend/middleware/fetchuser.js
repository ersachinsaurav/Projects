const jwt = require("jsonwebtoken");
const JWT_SECRET = "IamBEST";

const fetchuser = (req, res, next) => {
  // Get the user from jwt token and add id to req object
  const token = req.header("authToken");
  if (!token) {
    return res.status(401).json({ error: "Invalid token." });
  }
  try {
    const data = jwt.verify(token, JWT_SECRET);
    req.user = data.user;
    next();
  } catch (error) {
    console.log(error.message);
    return res.status(401).json({ error: "Invalid token." });
  }
};

module.exports = fetchuser;
