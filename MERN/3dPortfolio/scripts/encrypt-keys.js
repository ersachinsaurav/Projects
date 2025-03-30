import { fileURLToPath } from 'url';
import { dirname, join } from 'path';
import { readFileSync, writeFileSync } from 'fs';
import CryptoJS from 'crypto-js';
import dotenv from 'dotenv';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// Secure cleanup function
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

// Load environment variables
dotenv.config({ path: join(__dirname, '../.env.production') });

// Get configuration from environment variables
const getConfig = () => {
  const config = {
    keySize: 256 / 32,
    iterations: 10000,
    pepper: process.env.VITE_PEPPER,
    secretKey: process.env.VITE_SECRET_KEY
  };

  if (!config.pepper || !config.secretKey) {
    throw new Error('Missing required security configuration');
  }

  return config;
};

// Get the salt from environment variables
const getEnvironmentSalt = () => {
  const envSalt = process.env.VITE_SALT;
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
  try {
    const config = getConfig();
    const envSalt = getEnvironmentSalt();
    const peppered = config.pepper + config.secretKey + envSalt + operationSalt;
    return CryptoJS.PBKDF2(peppered, operationSalt, {
      keySize: config.keySize,
      iterations: config.iterations
    });
  } catch (error) {
    throw new Error('Failed to generate encryption key');
  }
};

const encrypt = (text) => {
  try {
    if (!text) throw new Error('Empty text provided for encryption');

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

    return `${operationSaltHex}:${ivHex}:${encryptedHex}`;
  } catch (error) {
    throw new Error(`Encryption failed: ${error.message}`);
  }
};

// Read .env.production
const envPath = join(__dirname, '../.env.production');
const configPath = join(__dirname, '../src/config/keys.js');

let env;
try {
  env = readFileSync(envPath, 'utf8');
} catch (error) {
  throw new Error(`Failed to read .env.production file: ${error.message}`);
}

const envVars = {};

// Parse env file
env.split('\n').forEach(line => {
  if (line && !line.startsWith('#')) {
    const [key, ...valueParts] = line.split('=');
    if (key && valueParts.length > 0) {
      envVars[key.trim()] = valueParts.join('=').trim();
    }
  }
});

// Validate required environment variables
const requiredVars = [
  'VITE_GITHUB_TOKEN',
  'VITE_APP_EMAILJS_SERVICE_ID',
  'VITE_APP_EMAILJS_TEMPLATE_ID',
  'VITE_APP_EMAILJS_PUBLIC_KEY',
  'VITE_SALT',
  'VITE_PEPPER',
  'VITE_SECRET_KEY'
];

const missingVars = requiredVars.filter(varName => !envVars[varName]);
if (missingVars.length > 0) {
  throw new Error('Missing required environment variables: ' + missingVars.join(', '));
}

// Create encrypted config
const encryptedConfig = {
  GITHUB_TOKEN: encrypt(envVars.VITE_GITHUB_TOKEN),
  EMAILJS_SERVICE_ID: encrypt(envVars.VITE_APP_EMAILJS_SERVICE_ID),
  EMAILJS_TEMPLATE_ID: encrypt(envVars.VITE_APP_EMAILJS_TEMPLATE_ID),
  EMAILJS_PUBLIC_KEY: encrypt(envVars.VITE_APP_EMAILJS_PUBLIC_KEY)
};

// Validate encrypted values
Object.entries(encryptedConfig).forEach(([key, value]) => {
  if (!value) {
    throw new Error(`Failed to encrypt ${key}`);
  }
});

// Update keys.js with encrypted values
const configContent = `import { decrypt } from '../utils/crypto';

const encryptedKeys = {
  GITHUB_TOKEN: '${encryptedConfig.GITHUB_TOKEN}',
  EMAILJS_SERVICE_ID: '${encryptedConfig.EMAILJS_SERVICE_ID}',
  EMAILJS_TEMPLATE_ID: '${encryptedConfig.EMAILJS_TEMPLATE_ID}',
  EMAILJS_PUBLIC_KEY: '${encryptedConfig.EMAILJS_PUBLIC_KEY}'
};

export const getKey = (keyName) => {
  try {
    const encryptedValue = encryptedKeys[keyName];
    if (!encryptedValue) return null;
    return decrypt(encryptedValue);
  } catch {
    return null;
  }
};`;

try {
  writeFileSync(configPath, configContent);
} catch (error) {
  throw new Error(`Failed to write config file: ${error.message}`);
}

// Clean up sensitive data from memory
secureErase(env);
secureErase(envVars);
secureErase(encryptedConfig);
