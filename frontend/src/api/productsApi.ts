import axios from "axios";

interface Product {
  // Define the fields of your Product interface
  id: string;
  name: string;
  price: number;
  description: string;
  country_of_origin: string;
  fruit_or_vegetable: string;
  expiry_date: string;
  file: string;
  imageId: string;
}

interface ProductResponse {
  product?: Product;
}

const BACKEND_URL = "http://localhost:8002";

export const fetchProducts = async (): Promise<Product[]> => {
  try {
    const response = await axios.get<ProductResponse>(
      `${BACKEND_URL}/api/products`,
    );

    const products = response.data.products;

    if (!products) {
      new Error("Product not found in the response");
    }

    console.log(products);

    return products
  } catch (error) {
    console.error("Error fetching products:", error);
    return [];
  }
};