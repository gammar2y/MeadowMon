import React, { useState } from 'react';

const Cart = () => {
  const [cartItems, setCartItems] = useState([]);

  const addItemToCart = (item) => {
    setCartItems([...cartItems, item]);
  };

  const removeItemFromCart = (index) => {
    const newCartItems = cartItems.filter((_, i) => i !== index);
    setCartItems(newCartItems);
  };

  return (
    <div>
      <h2>Shopping Cart</h2>
      <ul>
        {cartItems.map((item, index) => (
          <li key={index}>
            {item.name} - ${item.price}
            <button onClick={() => removeItemFromCart(index)}>Remove</button>
          </li>
        ))}
      </ul>
      <button onClick={() => addItemToCart({ name: 'Sample Item', price: 10 })}>
        Add Sample Item
      </button>
    </div>
  );
};

export default Cart;