import crypto from 'crypto';

const generateSecureKey = () => {
  return crypto.randomBytes(64).toString('hex');
};
