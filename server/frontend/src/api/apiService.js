const API_BASE_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8000';

export const fetchData = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/`);
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('There was a problem with the fetch operation:', error);
  }
};

export const postData = async (data) => {
  try {
    const response = await fetch(`${backendUrl}/order_confirmation`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    const result = await response.json();
    return result;
  } catch (error) {
    console.error('Post data failed:', error);
    throw error;
  }
};