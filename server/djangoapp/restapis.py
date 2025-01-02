"""
This module provides API interaction functions for the Django application.
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

backend_url = os.getenv('backend_url', default="http://localhost:3030")

def get_request(endpoint, **kwargs):
    """
    Args:
        endpoint (str): The API endpoint to append to the backend URL.
        **kwargs: Arbitrary keyword arguments to pass as query parameters.

    Returns:
        dict: The JSON response from the GET request.
    """
    params = ""
    if kwargs:
        params = "&".join(f"{key}={value}" for key, value in kwargs.items())

    request_url = f"{backend_url}{endpoint}?{params}"

    print(f"GET from {request_url}")
    try:
        response = requests.get(request_url)
        return response.json()
    except requests.RequestException:
        print("Network exception occurred")
        return None
