const express = require("express");
const router = express.Router();
const userController = require("../controllers/userController.js");
// const authMiddleware = require("../middleware/authMiddleware");

// Public routes
router.post("/register", userController.register);
console.log("req.body");
router.post("/login", userController.login);

// Protected routes
// router.use(authMiddleware);

module.exports = router;
