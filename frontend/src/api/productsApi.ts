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
            `${BACKEND_URL}/api/products/6775934ed79a82364c118356`
        );

        const product = response.data.product;

        if (!product) {
            new Error("Product not found in the response");
        }

        console.log(product);

        // Return an array of the product repeated multiple times
        return Array(36).fill(product);
    } catch (error) {
        console.error("Error fetching products:", error);
        return [];
    }
};
