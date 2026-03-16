import { useEffect, useState } from "react";
import { getCart, removeCart } from "../api/cartApi";
import { useNavigate } from "react-router-dom";

function Cart() {

  const [cart, setCart] = useState([]);
  const [total, setTotal] = useState(0);

  const navigate = useNavigate();

  const loadCart = async () => {

    try {

      const res = await getCart();

      setCart(res.data.items);
      setTotal(res.data.cart_total);

    } catch (err) {

      if (err.response && err.response.status === 401) {

        navigate("/login");

      } else {

        console.error(err);

      }

    }

  };

  useEffect(() => {

    loadCart();

  }, []);

  const removeItem = async (id) => {

    try {

      await removeCart(id);

      loadCart();

    } catch (err) {

      console.error(err);

    }

  };

  return (

    <div className="products-container">

      <h1 style={{marginBottom:"20px"}}>

        Your Cart

      </h1>

      {cart.length === 0 ? (

        <p>No items in cart</p>

      ) : (

        cart.map((item) => (

          <div key={item.product_id} className="product-card">

            <h3>{item.product_name}</h3>

            <p>Price: ${item.price}</p>

            <p>Quantity: {item.quantity}</p>

            <p>Total: ${item.total_price}</p>

            <button onClick={()=>removeItem(item.product_id)}>

              Remove Item

            </button>

          </div>

        ))

      )}

      <h2 style={{marginTop:"20px"}}>

        Cart Total: ${total}

      </h2>

    </div>

  );

}

export default Cart;