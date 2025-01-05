import React from "react";
import ProductCard from "../components/ProductCard";
import { Box } from "@mui/material";
import { useSelector } from "react-redux";
import { RootState } from "../redux/store";

const FilteredProductsList: React.FC = () => {
  const { filteredProducts, loading, error } = useSelector(
    (state: RootState) => state.products,
  );

  if (loading) return <div style={{ color: "black" }}>Ładowanie...</div>;
  if (error) return <div style={{ color: "black" }}>{error}</div>;

  return (
    <Box
      sx={{
        margin: "3rem",
        display: "grid",
        gridTemplateColumns: "repeat(auto-fill, minmax(300px, 1fr))",
        gap: 4,
      }}
    >
      {filteredProducts.length > 0 ? (
        filteredProducts.map((product, index) => (
          <ProductCard
            key={index}
            name={product.name}
            price={product.price}
            country_of_origin={product.country_of_origin}
            description={product.description}
            fruit_or_vegetable={product.fruit_or_vegetable}
            expiry_date={product.expiry_date}
            imageUrl={product.file}
            imageId={product.imageId}
            onAddToCart={() => console.log("Product added to cart")}
          />
        ))
      ) : (
        <p>No products available or no filters applied.</p>
      )}
    </Box>
  );
};

export default FilteredProductsList;