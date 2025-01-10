export interface Product {
  id: string;
  name: string;
  price: number;
  description: string;
  country_of_origin: string;
  is_vegetable: boolean;
  expiry_date: string;
  file: string;
}

export const BACKEND_URL = "http://localhost:8002";
