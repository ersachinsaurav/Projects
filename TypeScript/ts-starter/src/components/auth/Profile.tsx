import React from 'react';

export type ProfileProps = {
  name: string;
};

const Profile = ({ name }: ProfileProps) => {
  return (
    <div>
      <h2>Profile</h2>
      <h4>Profile Name: {name}</h4>
    </div>
  );
};

export default Profile;
