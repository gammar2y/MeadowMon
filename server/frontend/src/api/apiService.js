const backendUrl = process.env.REACT_APP_BACKEND_URL;

export const fetchData = async () => {
  try {
    const response = await fetch(`${backendUrl}/api/some-endpoint`);
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Fetch data failed:', error);
    throw error;
  }
};

export const postData = async (data) => {
  try {
    const response = await fetch(`${backendUrl}/api/some-endpoint`, {
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