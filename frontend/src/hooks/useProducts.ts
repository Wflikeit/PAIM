import { useState, useEffect } from "react";
import axios from "axios";


interface Product {
  name: string;
  price: string;
  country_of_origin: string;
  description: string;
  fruit_or_vegetable: string;
  expiry_date: string;
  imageId: string;
  imageUrl?: string;
}

interface ProductResponse {
  product?: Product;
}

const fetchProducts = async (): Promise<Product[]> => {
  try {
    
    const response = await axios.get<ProductResponse>(`http://localhost:8000/api/products/675dbc6fcea393dd5e2c6f83`);

    const product = response.data.product;

    if (product) {
      const imageResponse = await axios.get<Blob>(
        `http://localhost:8000/api/products/675dbc6fcea393dd5e2c6f83/image`,
        { responseType: "blob" }
      );
      const imageUrl = URL.createObjectURL(imageResponse.data);
      product.imageUrl = imageUrl;
      return [product];
    } else {
      return [];
    }
  } catch (error) {
    console.error("Error fetching products:", error);
    return [];
  }
};

const useProducts = () => {
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const getProducts = async () => {
      try {
        const data = await fetchProducts();
        setProducts(data);
      } catch (error) {
        setError("Failed to fetch products: " + error);
      } finally {
        setLoading(false);
      }
    };

    getProducts();
  }, []);

  return { products, loading, error };
};

export default useProducts;
