import React from "react";
import {
  Button,
  Card,
  CardContent,
  CardMedia,
  Typography,
} from "@mui/material";

interface ProductCardProps {
  id: string;
  name: string;
  price: number;
  country_of_origin: string;
  description: string;
  fruit_or_vegetable: string;
  imageId: string;
  expiry_date: string;
  imageUrl?: string;
  onAddToCart: () => void; // Add this property
}

const ProductCard: React.FC<ProductCardProps> = ({
  id,
  name,
  price,
  country_of_origin,
  description,
  fruit_or_vegetable,
  expiry_date,
  imageUrl,
  onAddToCart, // Use this property
}) => {
  return (
    <Card
      sx={{
        display: "flex",
        flexDirection: "column",
        height: "100%",
      }}
    >
      <CardMedia
        component="img"
        height="140"
        image={imageUrl || "https://via.placeholder.com/150"}
        alt={name}
      />
      <CardContent
        sx={{
          flexGrow: 1,
          display: "flex",
          flexDirection: "column",
          justifyContent: "space-between",
        }}
      >
        <Typography variant="h5" component="div">
          {name}
        </Typography>
        <Typography
          variant="body2"
          color="text.secondary"
          sx={{
            overflow: "hidden",
            textOverflow: "ellipsis",
            whiteSpace: "nowrap",
          }}
        >
          {description}
        </Typography>
        <Typography variant="body2" color="text.secondary">
          Kraj pochodzenia: {country_of_origin}
        </Typography>
        <Typography variant="body2" color="text.secondary">
          Typ: {fruit_or_vegetable}
        </Typography>
        <Typography variant="body2" color="text.secondary">
          Data ważności: {expiry_date}
        </Typography>
        <Typography variant="h6" color="text.primary">
          Cena: {price} zł
        </Typography>
        <Button
          className="add-to-cart"
          onClick={onAddToCart} // Handle add to cart
          variant="contained"
          color="primary"
        >
          Dodaj do koszyka
        </Button>
      </CardContent>
    </Card>
  );
};

export default ProductCard;