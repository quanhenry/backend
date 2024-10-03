const express = require("express");
const path = require("path");
// const cookieParser = require("cookie-parser");
const logger = require("morgan");
const mongoose = require("mongoose");

//const indexRouter = require("./routes/index");
const usersRouter = require("./routes/userRoutes");
// const apiRouter = require("./routes/api");
console.log("test ");
const app = express();
console.log("test 1");
// Connect to MongoDB
mongoose
  .connect("mongodb://localhost/myapp", {
    useNewUrlParser: true,
    useUnifiedTopology: true,
  })
  .then(() => console.log("MongoDB connected"))
  .catch((err) => console.error("MongoDB connection error:", err));

// View engine setup
app.set("views", path.join(__dirname, "views"));
app.set("view engine", "ejs");
console.log("test 2");
app.use(logger("dev"));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
// app.use(cookieParser());
app.use(express.static(path.join(__dirname, "public")));
console.log("test 3");
// Routes
// app.use("/", indexRouter);
console.log("app");
app.use("/users", usersRouter);
// app.use("/api", apiRouter);

// Error handler
app.use((err, req, res, next) => {
  res.status(err.status || 500);
  res.json({
    error: {
      message: err.message,
    },
  });
});
console.log("req.body");
module.exports = app;
