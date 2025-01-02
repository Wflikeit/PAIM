import useProducts from "../hooks/useProducts";
import ProductCard from "../components/ProductCard";
import { Box } from "@mui/material";

const ProductsList: React.FC = () => {
  const { products, loading, error } = useProducts();

  if (loading) return <div style={{ color: "black" }}>Ładowanie...</div>;
  if (error) return <div style={{ color: "black" }}>{error}</div>;

  return (
    <>
      <Box
        sx={{
          margin: "3rem",
          display: "grid",
          gridTemplateColumns: "repeat(auto-fill, minmax(300px, 1fr))",
          gap: 4,
        }}
      >
        {products.length > 0 ? (
          products.map((product, index) => (
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
          <p>
            Expected an array of products, but received:{" "}
            {JSON.stringify(products)}
          </p>
        )}
      </Box>
    </>
  );
};

export default ProductsList;