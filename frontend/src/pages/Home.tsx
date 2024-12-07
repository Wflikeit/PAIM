import React from "react";
import useProducts from "../hooks/useProducts";
import ProductCard from "../components/ProductCard";

const ProductsList = () => {
  const { products, loading, error } = useProducts();

  if (loading) return <div>Ładowanie...</div>;
  if (error) return <div>{error}</div>;

  return (
    <div>
      {products.length > 0 ? (
        products.map((product, index) => (
          <ProductCard
            key={index}
            name={product.name}
            price={product.price}
            country_of_origin={product.country_of_origin}
            description={product.description}
            fruit_or_vegetable={product.fruit_or_vegetable}
            imageId={product.imageId}
            expiry_date={product.expiry_date}
            onAddToCart={() => console.log("Product added to cart")}
          />
        ))
      ) : (
        <p>
          Expected an array of products, but received:{" "}
          {JSON.stringify(products)}
        </p>
      )}
    </div>
  );
};

export default ProductsList;
