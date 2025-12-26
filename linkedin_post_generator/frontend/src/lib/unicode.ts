/**
 * Unicode Text Formatting Utilities
 * ===================================
 * Functions for converting text to Unicode-styled characters
 * for LinkedIn posts (since LinkedIn doesn't support markdown).
 */

/**
 * Convert text to Unicode Mathematical Sans-Serif Bold
 */
export function toUnicodeBold(text: string): string {
  const boldUpperStart = 0x1D5D4;
  const boldLowerStart = 0x1D5EE;
  const boldDigitStart = 0x1D7EC;

  return Array.from(text).map(char => {
    if (char >= 'A' && char <= 'Z') {
      return String.fromCodePoint(boldUpperStart + (char.charCodeAt(0) - 'A'.charCodeAt(0)));
    } else if (char >= 'a' && char <= 'z') {
      return String.fromCodePoint(boldLowerStart + (char.charCodeAt(0) - 'a'.charCodeAt(0)));
    } else if (char >= '0' && char <= '9') {
      return String.fromCodePoint(boldDigitStart + (char.charCodeAt(0) - '0'.charCodeAt(0)));
    }
    return char;
  }).join('');
}

/**
 * Convert text to Unicode Mathematical Sans-Serif Italic
 */
export function toUnicodeItalic(text: string): string {
  const italicUpperStart = 0x1D608;
  const italicLowerStart = 0x1D622;

  return Array.from(text).map(char => {
    if (char >= 'A' && char <= 'Z') {
      return String.fromCodePoint(italicUpperStart + (char.charCodeAt(0) - 'A'.charCodeAt(0)));
    } else if (char >= 'a' && char <= 'z') {
      return String.fromCodePoint(italicLowerStart + (char.charCodeAt(0) - 'a'.charCodeAt(0)));
    }
    return char;
  }).join('');
}

/**
 * Add combining underline character after each character
 */
export function toUnicodeUnderline(text: string): string {
  return Array.from(text).map(char => char + '\u0332').join('');
}

/**
 * Add combining strikethrough character after each character
 */
export function toUnicodeStrikethrough(text: string): string {
  return Array.from(text).map(char => char + '\u0336').join('');
}

/**
 * Remove all Unicode formatting from text
 */
export function removeUnicodeFormatting(text: string): string {
  // Remove combining characters
  let result = text.replace(/[\u0332\u0336]/g, '');

  const boldUpperStart = 0x1D5D4;
  const boldLowerStart = 0x1D5EE;
  const boldDigitStart = 0x1D7EC;
  const italicUpperStart = 0x1D608;
  const italicLowerStart = 0x1D622;

  result = Array.from(result).map(char => {
    const code = char.codePointAt(0) || 0;

    // Bold uppercase
    if (code >= boldUpperStart && code < boldUpperStart + 26) {
      return String.fromCharCode('A'.charCodeAt(0) + (code - boldUpperStart));
    }
    // Bold lowercase
    if (code >= boldLowerStart && code < boldLowerStart + 26) {
      return String.fromCharCode('a'.charCodeAt(0) + (code - boldLowerStart));
    }
    // Bold digits
    if (code >= boldDigitStart && code < boldDigitStart + 10) {
      return String.fromCharCode('0'.charCodeAt(0) + (code - boldDigitStart));
    }
    // Italic uppercase
    if (code >= italicUpperStart && code < italicUpperStart + 26) {
      return String.fromCharCode('A'.charCodeAt(0) + (code - italicUpperStart));
    }
    // Italic lowercase
    if (code >= italicLowerStart && code < italicLowerStart + 26) {
      return String.fromCharCode('a'.charCodeAt(0) + (code - italicLowerStart));
    }

    return char;
  }).join('');

  return result;
}

