const API_BASE_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8000';

export const fetchData = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/data`);
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
    const response = await fetch(`${API_BASE_URL}/api/order_confirmation`, {
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

export const registerUser = async (userData) => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/register`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(userData),
    });
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    const result = await response.json();
    return result;
  } catch (error) {
    console.error('User registration failed:', error);
    throw error;
  }
};

export const loginUser = async (credentials) => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(credentials),
    });
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    const result = await response.json();
    return result;
  } catch (error) {
    console.error('User login failed:', error);
    throw error;
  }
};

export const logoutUser = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/logout`, {
      method: 'POST',
    });
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    return { success: true };
  } catch (error) {
    console.error('User logout failed:', error);
    throw error;
  }
};

export const fetchProductDetails = async (productId) => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/get_product_details/${productId}`);
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('There was a problem with the fetch operation:', error);
  }
};