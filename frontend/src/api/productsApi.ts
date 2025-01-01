import axios from "axios";

interface ProductResponse {
    product?: Product;
}

const BACKEND_URL = "http://localhost:8002";
export const fetchProducts = async (): Promise<Product[]> => {
    try {
        const response = await axios.get<ProductResponse>(
            `${BACKEND_URL}/api/products/6775934ed79a82364c118356`,
        );
        console.log(response.data.product);
        return [
            response.data.product,
            response.data.product,
            response.data.product,
            response.data.product,
        ];
    } catch (error) {
        console.error("Error fetching products:", error);
        return [];
    }
};