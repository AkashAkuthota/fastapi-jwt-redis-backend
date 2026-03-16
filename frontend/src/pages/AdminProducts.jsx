import { useEffect, useState } from "react";
import { getProducts, createProduct, deleteProduct, updateProduct } from "../api/productApi";
import { toast } from "react-toastify";

function AdminProducts() {

  const [products,setProducts] = useState([]);

  const [name,setName] = useState("");
  const [description,setDescription] = useState("");
  const [price,setPrice] = useState("");
  const [quantity,setQuantity] = useState("");

  const [editingId,setEditingId] = useState(null);
  const [editData,setEditData] = useState({});

  const loadProducts = async () => {

    try {

      const res = await getProducts();

      setProducts(res.data);

    } catch {

      toast.error("Failed to load products");

    }

  };

  useEffect(() => {

    loadProducts();

  }, []);

  const handleCreate = async (e) => {

    e.preventDefault();

    try {

      await createProduct({
        name,
        description,
        price:Number(price),
        quantity:Number(quantity)
      });

      toast.success("Product created successfully");

      setName("");
      setDescription("");
      setPrice("");
      setQuantity("");

      loadProducts();

    } catch {

      toast.error("Failed to create product");

    }

  };

  const handleDelete = async (id) => {

    if (!window.confirm("Delete this product?")) return;

    try {

      await deleteProduct(id);

      toast.success("Product deleted");

      loadProducts();

    } catch {

      toast.error("Delete failed");

    }

  };

  const startEdit = (product) => {

    setEditingId(product.id);

    setEditData({
      name: product.name,
      description: product.description,
      price: product.price,
      quantity: product.quantity
    });

  };

  const handleUpdate = async (id) => {

    try {

      await updateProduct(id, editData);

      toast.success("Product updated");

      setEditingId(null);

      loadProducts();

    } catch {

      toast.error("Update failed");

    }

  };

  return (

    <div className="products-container">

      <h1>Admin Product Dashboard</h1>

      <form className="admin-form" onSubmit={handleCreate}>

        <input
          placeholder="Product Name"
          value={name}
          onChange={(e)=>setName(e.target.value)}
        />

        <input
          placeholder="Description"
          value={description}
          onChange={(e)=>setDescription(e.target.value)}
        />

        <input
          placeholder="Price"
          value={price}
          onChange={(e)=>setPrice(e.target.value)}
        />

        <input
          placeholder="Quantity"
          value={quantity}
          onChange={(e)=>setQuantity(e.target.value)}
        />

        <button type="submit">
          Create Product
        </button>

      </form>

      <div className="products-grid">

        {products.map((product)=>{

          const isEditing = editingId === product.id;

          return (

            <div key={product.id} className="product-card">

              {isEditing ? (

                <>
                  <input
                    value={editData.name}
                    onChange={(e)=>setEditData({...editData,name:e.target.value})}
                  />

                  <input
                    value={editData.description}
                    onChange={(e)=>setEditData({...editData,description:e.target.value})}
                  />

                  <input
                    value={editData.price}
                    onChange={(e)=>setEditData({...editData,price:e.target.value})}
                  />

                  <input
                    value={editData.quantity}
                    onChange={(e)=>setEditData({...editData,quantity:e.target.value})}
                  />

                  <button onClick={()=>handleUpdate(product.id)}>
                    Update
                  </button>

                </>

              ) : (

                <>
                  <h3>{product.name}</h3>

                  <p>{product.description}</p>

                  <p>Price: ${product.price}</p>

                  <p>Stock: {product.quantity}</p>

                  <button
                    style={{marginRight:"10px"}}
                    onClick={()=>startEdit(product)}
                  >
                    Edit
                  </button>

                  <button
                    style={{background:"#dc2626"}}
                    onClick={()=>handleDelete(product.id)}
                  >
                    Delete
                  </button>

                </>

              )}

            </div>

          );

        })}

      </div>

    </div>

  );

}

export default AdminProducts;