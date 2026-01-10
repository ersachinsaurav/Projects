/**
 * Unicode Text Formatting Utilities
 * =================================
 * Optimized, centralized, and extensible Unicode formatting helpers
 * for platforms like LinkedIn (no markdown support).
 */

/* ------------------------------------------------------------------ */
/* Unicode Metadata (Single Source of Truth)                           */
/* ------------------------------------------------------------------ */

const UNICODE = {
  bold: {
    upper: 0x1d5d4,
    lower: 0x1d5ee,
    digit: 0x1d7ec
  },
  italic: {
    upper: 0x1d608,
    lower: 0x1d622
  },
  boldItalic: {
    upper: 0x1d63c,
    lower: 0x1d656
  },
  underline: '\u0332',
  strike: '\u0336'
};

const ASCII = {
  A: 65,
  a: 97,
  zero: 48
};

/* ------------------------------------------------------------------ */
/* Generic Unicode Mapper                                              */
/* ------------------------------------------------------------------ */

type UnicodeRanges = {
  upper?: number;
  lower?: number;
  digit?: number;
};

function mapUnicode(text: string, ranges: UnicodeRanges): string {
  return Array.from(text, char => {
    const code = char.codePointAt(0)!;

    if (ranges.upper && char >= 'A' && char <= 'Z') {
      return String.fromCodePoint(ranges.upper + code - ASCII.A);
    }
    if (ranges.lower && char >= 'a' && char <= 'z') {
      return String.fromCodePoint(ranges.lower + code - ASCII.a);
    }
    if (ranges.digit && char >= '0' && char <= '9') {
      return String.fromCodePoint(ranges.digit + code - ASCII.zero);
    }
    return char;
  }).join('');
}

/* ------------------------------------------------------------------ */
/* Style Application Helpers                                           */
/* ------------------------------------------------------------------ */

export const toUnicodeBold = (text: string) =>
  mapUnicode(text, UNICODE.bold);

export const toUnicodeItalic = (text: string) =>
  mapUnicode(text, UNICODE.italic);

export const toUnicodeBoldItalic = (text: string) =>
  mapUnicode(text, { ...UNICODE.boldItalic, digit: UNICODE.bold.digit });

export const toUnicodeUnderline = (text: string) =>
  Array.from(text, char => char + UNICODE.underline).join('');

export const toUnicodeStrikethrough = (text: string) =>
  Array.from(text, char => char + UNICODE.strike).join('');

/* ------------------------------------------------------------------ */
/* Formatting Detection (Single Pass)                                  */
/* ------------------------------------------------------------------ */
export function detectFormatting(text: string) {
  let hasBold = false;
  let hasItalic = false;
  let hasBoldItalic = false;

  for (const char of text) {
    const code = char.codePointAt(0)!;

    if (
      (code >= UNICODE.boldItalic.upper && code < UNICODE.boldItalic.upper + 26) ||
      (code >= UNICODE.boldItalic.lower && code < UNICODE.boldItalic.lower + 26)
    ) {
      hasBoldItalic = true;
      hasBold = true;
      hasItalic = true;
      continue;
    }

    if (
      (code >= UNICODE.bold.upper && code < UNICODE.bold.upper + 26) ||
      (code >= UNICODE.bold.lower && code < UNICODE.bold.lower + 26) ||
      (code >= UNICODE.bold.digit && code < UNICODE.bold.digit + 10)
    ) {
      hasBold = true;
    }

    if (
      (code >= UNICODE.italic.upper && code < UNICODE.italic.upper + 26) ||
      (code >= UNICODE.italic.lower && code < UNICODE.italic.lower + 26)
    ) {
      hasItalic = true;
    }
  }

  return {
    bold: hasBold,
    italic: hasItalic,
    boldItalic: hasBoldItalic,
    underline: text.includes(UNICODE.underline),
    strike: text.includes(UNICODE.strike)
  };
}

/* ------------------------------------------------------------------ */
/* Remove All Unicode Formatting                                       */
/* ------------------------------------------------------------------ */

export function removeUnicodeFormatting(text: string): string {
  const stripped = text.replace(
    new RegExp(`[${UNICODE.underline}${UNICODE.strike}]`, 'g'),
    ''
  );

  return Array.from(stripped, char => {
    const code = char.codePointAt(0)!;

    const decode = (
      start: number,
      base: number,
      count: number
    ) => (code >= start && code < start + count)
      ? String.fromCharCode(base + (code - start))
      : null;

    return (
      decode(UNICODE.boldItalic.upper, ASCII.A, 26) ??
      decode(UNICODE.boldItalic.lower, ASCII.a, 26) ??
      decode(UNICODE.bold.upper, ASCII.A, 26) ??
      decode(UNICODE.bold.lower, ASCII.a, 26) ??
      decode(UNICODE.bold.digit, ASCII.zero, 10) ??
      decode(UNICODE.italic.upper, ASCII.A, 26) ??
      decode(UNICODE.italic.lower, ASCII.a, 26) ??
      char
    );
  }).join('');
}

/* ------------------------------------------------------------------ */
/* Deterministic Style Reapplication                                   */
/* ------------------------------------------------------------------ */

type StyleState = {
  bold?: boolean;
  italic?: boolean;
  underline?: boolean;
  strike?: boolean;
};

function applyStyles(text: string, styles: StyleState): string {
  let result = text;

  if (styles.bold && styles.italic) {
    result = toUnicodeBoldItalic(result);
  } else if (styles.bold) {
    result = toUnicodeBold(result);
  } else if (styles.italic) {
    result = toUnicodeItalic(result);
  }

  if (styles.underline) result = toUnicodeUnderline(result);
  if (styles.strike) result = toUnicodeStrikethrough(result);

  return result;
}

/* ------------------------------------------------------------------ */
/* Toggle Functions                                                    */
/* ------------------------------------------------------------------ */

export function toggleBold(text: string): string {
  const f = detectFormatting(text);
  return applyStyles(removeUnicodeFormatting(text), {
    bold: !f.bold,
    italic: f.italic,
    underline: f.underline,
    strike: f.strike
  });
}

export function toggleItalic(text: string): string {
  const f = detectFormatting(text);
  return applyStyles(removeUnicodeFormatting(text), {
    bold: f.bold,
    italic: !f.italic,
    underline: f.underline,
    strike: f.strike
  });
}

export function toggleUnderline(text: string): string {
  const f = detectFormatting(text);
  return applyStyles(removeUnicodeFormatting(text), {
    bold: f.bold,
    italic: f.italic,
    underline: !f.underline,
    strike: f.strike
  });
}

export function toggleStrikethrough(text: string): string {
  const f = detectFormatting(text);
  return applyStyles(removeUnicodeFormatting(text), {
    bold: f.bold,
    italic: f.italic,
    underline: f.underline,
    strike: !f.strike
  });
}
