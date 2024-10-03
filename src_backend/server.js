const express = require("express");
const app = require("./app");
const port = process.env.PORT || 5001;

app.use(express.json());
app.get("/", (req, res) => {
  res.send("Hello from the backend!");
});
console.log("server");
app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});
