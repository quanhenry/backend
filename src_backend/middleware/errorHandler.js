const errorHandler = (err, req, res, next) => {
  let statusCode = res.statusCode === 200 ? 500 : res.statusCode;
  let message = err.message;

  // Xử lý lỗi Mongoose ObjectId không hợp lệ
  if (err.name === "CastError" && err.kind === "ObjectId") {
    statusCode = 404;
    message = "Không tìm thấy tài nguyên";
  }

  // Xử lý lỗi trùng lặp khóa Mongoose
  if (err.code === 11000) {
    statusCode = 400;
    message = "Dữ liệu đã tồn tại";
  }

  // Xử lý lỗi xác thực Mongoose
  if (err.name === "ValidationError") {
    statusCode = 400;
    message = Object.values(err.errors)
      .map((val) => val.message)
      .join(", ");
  }

  res.status(statusCode).json({
    message: message,
    stack: process.env.NODE_ENV === "production" ? null : err.stack,
  });
};

module.exports = errorHandler;
