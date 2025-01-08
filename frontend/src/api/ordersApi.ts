import axios from "axios";

export const placeOrder = (orderDetails: any) => {
  return axios.post("/api/order", orderDetails);
};