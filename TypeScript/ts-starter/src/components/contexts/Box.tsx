import React, { useContext } from 'react';
import { ThemeContext } from './ThemeContext';

export default function Box() {
  const theme = useContext(ThemeContext);

  return (
    <div>
      <div
        style={{ background: theme.primary.main, color: theme.primary.text }}
      >
        Box
      </div>
      <div
        style={{
          background: theme.secondary.main,
          color: theme.secondary.text,
        }}
      >
        Box
      </div>
    </div>
  );
}
