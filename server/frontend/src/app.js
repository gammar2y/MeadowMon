import LoginPanel from "./components/login"
import Register from "./components/signup"
import { Routes, Route } from "react-router-dom";
import get_product from './store/product';
import cart from "./store/cart";
import checkout from "./store/checkout";
import order_confirmation from "./store/orders";
import requests from “./store/requests”;
import get_product_details from “./store/product”;
function App() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPanel />} />
      <Route path="/register" element={<Register />} />
      <Route path="/cart" element={<Cart/>} />
      <Route path="/checkout" element={<Checkout/>} />
      <Route path="/requests" element={<Requests/>} />
      <Route path="/order_confirmation" element={<Order_Confirmation/>} />
      <Route path="/get_product" element={<Get_Product/>} />
      <Route path="/get_product_details/:id" element={<Get_Product_Details/>} />
          </Routes>
  );
}
export default App;

