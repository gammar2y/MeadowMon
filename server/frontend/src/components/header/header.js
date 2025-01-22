import React from 'react';

const Header = () => {
  const backendUrl = process.env.REACT_APP_BACKEND_URL;
  console.log(`Backend URL: ${backendUrl}`);

  return (
    <header>
      <h1>Welcome to the App</h1>
      <p>Backend URL: {backendUrl}</p>
    </header>
  );
};

export default Header;