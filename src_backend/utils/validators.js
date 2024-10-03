const validator = require("validator");

const validateRegistration = (userData) => {
  const errors = {};

  if (!validator.isEmail(userData.email)) {
    errors.email = "Email không hợp lệ";
  }

  if (!validator.isLength(userData.password, { min: 8 })) {
    errors.password = "Mật khẩu phải có ít nhất 8 ký tự";
  }

  if (userData.password !== userData.confirmPassword) {
    errors.confirmPassword = "Mật khẩu xác nhận không khớp";
  }

  if (!validator.isLength(userData.username, { min: 3, max: 30 })) {
    errors.username = "Tên người dùng phải có từ 3 đến 30 ký tự";
  }

  return {
    errors,
    isValid: Object.keys(errors).length === 0,
  };
};

const validateLogin = (userData) => {
  const errors = {};

  if (!validator.isEmail(userData.email)) {
    errors.email = "Email không hợp lệ";
  }

  if (validator.isEmpty(userData.password)) {
    errors.password = "Mật khẩu không được để trống";
  }

  return {
    errors,
    isValid: Object.keys(errors).length === 0,
  };
};

const validateProfile = (profileData) => {
  const errors = {};

  if (!validator.isLength(profileData.bio, { max: 500 })) {
    errors.bio = "Tiểu sử không được vượt quá 500 ký tự";
  }

  if (!validator.isURL(profileData.website)) {
    errors.website = "URL website không hợp lệ";
  }

  return {
    errors,
    isValid: Object.keys(errors).length === 0,
  };
};

module.exports = {
  validateRegistration,
  validateLogin,
  validateProfile,
};
