import { addToCart } from "../api/cartApi";
import { useNavigate } from "react-router-dom";
import { toast } from "react-toastify";

function ProductCard({ product }) {

  const navigate = useNavigate();

  const handleAdd = async () => {

    try {

      await addToCart({
        product_id: product.id,
        quantity: 1
      });

      toast.success(`${product.name} added to cart`);

    } catch (err) {

      if (err.response?.status === 401) {

        toast.warning("Please login to add items");

        navigate("/login");

      } else {

        toast.error("Failed to add item");

      }

    }

  };

  return (

    <div className="product-card">

      <h3>{product.name}</h3>

      <p>{product.description}</p>

      <p>${product.price}</p>

      <p>Stock: {product.quantity}</p>

      <button onClick={handleAdd}>
        Add To Cart
      </button>

    </div>

  );

}

export default ProductCard;