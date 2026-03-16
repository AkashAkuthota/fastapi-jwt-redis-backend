import { useEffect, useState } from "react";
import { getProducts } from "../api/productApi";
import ProductCard from "../components/ProductCard";

function Products() {

  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);

  const loadProducts = async () => {

    try {

      const res = await getProducts();

      setProducts(res.data);

    } catch (err) {

      console.error(err);

    } finally {

      setLoading(false);

    }

  };

  useEffect(() => {

    loadProducts();

  }, []);

  if (loading) {

    return (

      <div className="products-container">

        <h1>Loading products...</h1>

      </div>

    );

  }

  return (

    <div className="products-container">

      <div className="hero">

        <div>

          <h1>Inventory Dashboard</h1>

          <p>Browse products and manage items in your inventory system</p>

          <p>{products.length} products available</p>

        </div>

      </div>

      <div className="products-grid">

        {products.map((product) => (

          <ProductCard key={product.id} product={product} />

        ))}

      </div>

    </div>

  );

}

export default Products;