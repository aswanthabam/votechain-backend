const crypto = require("crypto")

function deriveAesKeyFromOTP(otp, salt) {
  const iterations = 100000;
  const keyLength = 32; // 256 bits
  const digest = 'sha256';

  return crypto.pbkdf2Sync(otp, salt, iterations, keyLength, digest);
}

function decryptMessage(encryptedMessage, otp) {
  const [salt, iv, encrypted] = encryptedMessage.split(':').map((part) => Buffer.from(part, 'hex'));

  const aesKey = deriveAesKeyFromOTP(otp, salt);
  const decipher = crypto.createDecipheriv('aes-256-cbc', aesKey, iv);

  let decrypted = decipher.update(encrypted, 'hex', 'utf8');
  decrypted += decipher.final('utf8');

  return decrypted;
}