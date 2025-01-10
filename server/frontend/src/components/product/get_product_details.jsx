import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import "./GetProductDetails.css";

const GetProductDetails = () => {
  const { id } = useParams();
  const [product, setProduct] = useState(null);

  useEffect(() => {
    // Replace with your actual API call
    fetch(`/api/products/${id}`)
      .then(response => response.json())
      .then(data => setProduct(data))
      .catch(error => console.error('Error fetching product:', error));
  }, [id]);

  if (!product) {
    return <div>Loading...</div>;
  }

  return (
    <div className="product-details">
      <img src={product.image} alt={product.name} className="product-image" />
      <h2 className="product-name">{product.name}</h2>
      <p className="product-description">{product.description}</p>
      <p className="product-price">${product.price}</p>
    </div>
  );
};

export default GetProductDetails;