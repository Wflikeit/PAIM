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
