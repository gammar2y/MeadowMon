import React, { useState, useEffect } from 'react';
import { fetchData } from './api/apiService';
import Header from './components/header/header.js';

const App = () => {
  const [data, setData] = useState(null);

  useEffect(() => {
    const getData = async () => {
      const result = await fetchData();
      setData(result);
    };
    getData();
  }, []);

  return (
    <div>
      <Header />
      <div>{data ? JSON.stringify(data) : 'Loading data...'}</div>
    </div>
  );
};

export default App;

