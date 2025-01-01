import LoginPanel from "./components/Login/Login"
import Register from "./components/Register/Register"
import { Routes, Route } from "react-router-dom";
import get_product from './components/Product/get_product';
import cart from "./components/orders/cart";
import checkout from "./components/orders/checkout";
import order_confirmation from "./components/orders/order_confirmation";
import cart from "./components/orders/cart";
import requests from “./components/requests/requests”;
import get_product_details from “./components/Product/get_product_details”;
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

