const nodemailer = require("nodemailer");
const config = require("../config/email");

const transporter = nodemailer.createTransport({
  host: config.host,
  port: config.port,
  secure: config.secure,
  auth: {
    user: config.user,
    pass: config.pass,
  },
});

const sendEmail = async (to, subject, text, html) => {
  try {
    const info = await transporter.sendMail({
      from: config.from,
      to: to,
      subject: subject,
      text: text,
      html: html,
    });
    console.log("Email sent: ", info.messageId);
    return info;
  } catch (error) {
    console.error("Error sending email: ", error);
    throw error;
  }
};

const sendPasswordResetEmail = async (to, resetToken) => {
  const subject = "Password Reset Request";
  const text = `Please use the following link to reset your password: ${config.baseUrl}/reset-password/${resetToken}`;
  const html = `<p>Please use the following link to reset your password:</p>
                <a href="${config.baseUrl}/reset-password/${resetToken}">Reset Password</a>`;

  return sendEmail(to, subject, text, html);
};

const sendWelcomeEmail = async (to, username) => {
  const subject = "Welcome to Our Platform";
  const text = `Welcome ${username}! Thank you for joining our platform.`;
  const html = `<h1>Welcome ${username}!</h1><p>Thank you for joining our platform.</p>`;

  return sendEmail(to, subject, text, html);
};

module.exports = {
  sendEmail,
  sendPasswordResetEmail,
  sendWelcomeEmail,
};
