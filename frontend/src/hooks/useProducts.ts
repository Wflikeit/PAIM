import { useQuery } from "react-query";
import axios from "axios";
import { Product } from "../api/productsApi";

const BACKEND_URL = "http://localhost:8002";

const fetchProductsFromApi = async (): Promise<Product[]> => {
  const response = await axios.get<{ products: Product[] }>(
    `${BACKEND_URL}/api/products`,
  );
  if (!response.data.products) {
    throw new Error("Products not found in the response");
  }
  return response.data.products;
};

export const useProducts = () => {
  return useQuery("products", fetchProductsFromApi);
};