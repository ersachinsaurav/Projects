import CryptoJS from 'crypto-js';

// Get configuration from environment variables
const getConfig = () => {
  const config = {
    keySize: 256 / 32,
    iterations: 10000,
    pepper: import.meta.env.VITE_PEPPER,
    secretKey: import.meta.env.VITE_SECRET_KEY
  };

  if (!config.pepper || !config.secretKey) {
    throw new Error('Missing required security configuration');
  }

  return config;
};

// Get the salt from environment variables
const getEnvironmentSalt = () => {
  const envSalt = import.meta.env.VITE_SALT;
  if (!envSalt) {
    throw new Error('VITE_SALT environment variable is required');
  }
  return envSalt;
};

// Generate a unique IV for each encryption
const generateIV = () => {
  return CryptoJS.lib.WordArray.random(16);
};

// Generate a strong key from password, salt, and pepper
const generateKey = (operationSalt) => {
  const config = getConfig();
  const envSalt = getEnvironmentSalt();
  const peppered = config.pepper + config.secretKey + envSalt + operationSalt;
  return CryptoJS.PBKDF2(peppered, operationSalt, {
    keySize: config.keySize,
    iterations: config.iterations
  });
};

export const encrypt = (text) => {
  try {
    if (!text) return '';

    // Generate a unique salt for this encryption
    const operationSalt = CryptoJS.lib.WordArray.random(128 / 8);
    const iv = generateIV();
    const key = generateKey(operationSalt);

    // Encrypt the data
    const encrypted = CryptoJS.AES.encrypt(text, key, {
      iv: iv,
      mode: CryptoJS.mode.CBC,
      padding: CryptoJS.pad.Pkcs7
    });

    // Combine the operation salt, IV, and encrypted data
    const operationSaltHex = operationSalt.toString();
    const ivHex = iv.toString();
    const encryptedHex = encrypted.toString();

    // Secure cleanup
    secureErase({ key, operationSalt, iv });

    // Return combined string with delimiters
    return `${operationSaltHex}:${ivHex}:${encryptedHex}`;
  } catch (error) {
    return '';
  }
};

export const decrypt = (encryptedData) => {
  try {
    if (!encryptedData) return '';

    // Split the combined string
    const [operationSaltHex, ivHex, encryptedHex] = encryptedData.split(':');
    if (!operationSaltHex || !ivHex || !encryptedHex) {
      throw new Error('Invalid encrypted data format');
    }

    // Convert hex strings back to WordArrays
    const operationSalt = CryptoJS.enc.Hex.parse(operationSaltHex);
    const iv = CryptoJS.enc.Hex.parse(ivHex);
    const key = generateKey(operationSalt);

    // Decrypt the data
    const decrypted = CryptoJS.AES.decrypt(encryptedHex, key, {
      iv: iv,
      mode: CryptoJS.mode.CBC,
      padding: CryptoJS.pad.Pkcs7
    });

    // Secure cleanup
    secureErase({ key, operationSalt, iv });

    return decrypted.toString(CryptoJS.enc.Utf8);
  } catch (error) {
    return '';
  }
};

// Secure key erasure function
const secureErase = (obj) => {
  if (typeof obj === 'string') {
    const len = obj.length;
    for (let i = 0; i < len; i++) {
      obj = obj.replace(obj[i], '*');
    }
  } else if (typeof obj === 'object' && obj !== null) {
    Object.keys(obj).forEach(key => {
      secureErase(obj[key]);
    });
  }
};
