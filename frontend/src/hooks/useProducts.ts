import { useState, useEffect } from "react";
import axios from "axios";
import header from "../components/Header.tsx";
import {config} from "typescript-eslint";

interface Product {
  name: string;
  price: number;
  country_of_origin: string;
  description: string;
  fruit_or_vegetable: string;
  expiry_date: string;
  imageId: string;
  file?: string;
}

interface ProductResponse {
  product?: Product;
}

const fetchProducts = async (): Promise<Product[]> => {
  try {
    const response = await axios.get<ProductResponse>(
      `http://localhost:8002/api/products/6775934ed79a82364c118356`,
        // {headers: {Access-Control-Allow-Origin: "*"}}


    );
    console.log(response.data);
    console.log(response.data.product);
    return   [response.data.product]

    // return ;

    // if (product) {
    //   const imageResponse = await axios.get<Blob>(
    //     `http://localhost:8000/api/products/6772091ea203351edda37ccf/image`,
    //     { responseType: "blob" },
    //   );
    //   const imageUrl = URL.createObjectURL(imageResponse.data);
    //   product.imageUrl = imageUrl;
    //   return [product];
    // } else {
    //   return [];
    // }
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
        console.log(data);
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
