import LoginPanel from "./components/login/login"
import Register from "./components/signup/signup"
import { Routes, Route } from "react-router-dom";
import Product from './components/product/product';
import Cart from "./components/cart/cart";
import Checkout from "./components/checkout/checkout";
import PlaceOrder from "./components/orders/order";
import Get_Product_Details from "./components/product/get_product_details";
function App() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPanel />} />
      <Route path="/register" element={<Register />} />
      <Route path="/cart" element={<Cart/>} />
      <Route path="/checkout" element={<Checkout/>} />
      <Route path="/order_confirmation" element={<PlaceOrder/>} />
      <Route path="/get_product" element={<Product/>} />
      <Route path="/get_product_details/:id" element={<Get_Product_Details/>} />
          </Routes>
  );
}
export default App;

