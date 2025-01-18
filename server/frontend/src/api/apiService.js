import config from '../config';

export const fetchData = async () => {
  try {
    const response = await fetch(`${config.backendUrl}/api/data`);
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error fetching data:', error);
  }
};