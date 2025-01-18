import React from 'react';
import config from '../config';

const Header = () => {
  console.log('Backend URL in Header:', config.backendUrl); // This should print the URL
  return <header>Header Component</header>;
};

export default Header;