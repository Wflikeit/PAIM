import axios from "axios";

export interface Product {
  id: string;
  name: string;
  price: number;
  description: string;
  country_of_origin: string;
  fruit_or_vegetable: string;
  expiry_date: string;
  file: string;
}

export const BACKEND_URL = "http://localhost:8002";

export const fetchProductsFromApi = async (): Promise<Product[]> => {
  try {
    const response = await axios.get<{ products: Product[] }>(
      `${BACKEND_URL}/api/products`,
    );

    const products = response.data.products;
    console.log("Products fetched from the API:", products);

    if (!products) {
      throw new Error("Products not found in the response");
    }

    return products;
  } catch (error) {
    console.error("Error fetching products:", error);
    throw error; // Let Redux handle the error
  }
};
