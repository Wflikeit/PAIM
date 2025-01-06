import React from "react";
import ProductCard from "../components/ProductCard";
import { Box } from "@mui/material";
import { useDispatch, useSelector } from "react-redux";
import { RootState } from "../redux/store";
import { useProducts } from "../hooks/useProducts.ts";
import { addToCart } from "../model/cardItem"; // Import the addToCart action

const ProductsList: React.FC = () => {
  const { filters } = useSelector((state: RootState) => state.products);
  const { data: products = [], isLoading, error } = useProducts();
  const dispatch = useDispatch();

  const filteredProducts = products.filter((product) => {
    const matchesFruitOrVegetable =
      filters.fruitOrVegetable.length === 0 ||
      filters.fruitOrVegetable.includes(product.fruit_or_vegetable);

    const matchesCountryOfOrigin =
      filters.countryOfOrigin.length === 0 ||
      filters.countryOfOrigin.includes(product.country_of_origin);

    return matchesFruitOrVegetable && matchesCountryOfOrigin;
  });

  if (isLoading) return <div>Loading...</div>;
  if (error instanceof Error) return <div>Error: {error.message}</div>;

  return (
    <Box
      sx={{
        margin: "3rem",
        display: "grid",
        gridTemplateColumns: "repeat(auto-fill, minmax(300px, 1fr))",
        gap: 4,
      }}
    >
      {filteredProducts.map((product) => (
        <ProductCard
          id={product.id}
          key={product.id}
          name={product.name}
          price={product.price}
          country_of_origin={product.country_of_origin}
          description={product.description}
          fruit_or_vegetable={product.fruit_or_vegetable}
          expiry_date={product.expiry_date}
          imageUrl={product.file}
          imageId={product.imageId}
          onAddToCart={() => {
            dispatch(
              addToCart({
                id: product.id,
                name: product.name,
                price: product.price,
                quantity: 1, // Default quantity to add
              }),
            );
          }}
        />
      ))}
    </Box>
  );
};

export default ProductsList;