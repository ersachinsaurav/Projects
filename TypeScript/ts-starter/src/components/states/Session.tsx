import React, { useState } from 'react';

export default function Session() {
  const [isLoggedIn, toggleLoggedIn] = useState(false);

  const handleLogin = () => {
    toggleLoggedIn(true);
  };

  const handleLogout = () => {
    toggleLoggedIn(false);
  };

  return (
    <div>
      <button onClick={handleLogin}>Login</button>
      <button onClick={handleLogout}>Logout</button>
      <div>{isLoggedIn ? 'Logged In' : 'Logged Out'}</div>
    </div>
  );
}
