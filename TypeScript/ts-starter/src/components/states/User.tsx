import React, { useState } from 'react';

type AuthUser = {
  name: string;
  email: string;
};

export default function User() {
  // Type assertion
  // const [user, setUser] = useState<AuthUser>({} as AuthUser);
  const [user, setUser] = useState<AuthUser | null>(null);

  const handleLogin = () => {
    setUser({ name: 'Sachin', email: 'sachin@gmail.com' });
  };

  const handleLogout = () => {
    setUser(null);
  };

  return (
    <div>
      <button onClick={handleLogin}>Login</button>
      <button onClick={handleLogout}>Logout</button>
      <div>{`Name: ${user?.name}`}</div>
      <div>{`Email: ${user?.email}`}</div>
    </div>
  );
}
