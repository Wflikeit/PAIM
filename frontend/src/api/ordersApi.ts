import axios from "axios";
import { BACKEND_URL } from "../hooks/useProducts.ts";

export const placeOrder = (orderDetails: any) => {
  return axios.post(BACKEND_URL + "/api/purchase", orderDetails);
};
