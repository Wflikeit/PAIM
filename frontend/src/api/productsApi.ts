export interface Product {
  id: string;
  name: string;
  price: number;
  description: string;
  country_of_origin: string;
  fruit_or_vegetable: string;
  expiry_date: string;
  file: string;
  is_vegetable: string;
}

export const BACKEND_URL = "http://localhost:8002";
