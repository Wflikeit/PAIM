import React from "react";
import {
  Card,
  CardContent,
  Typography,
  Button,
  CardMedia,
} from "@mui/material";

interface ProductCardProps {
  name: string;
  price: number;
  country_of_origin: string;
  description: string;
  fruit_or_vegetable: string;
  imageId: string;
  expiry_date: string;
  imageUrl?: string;
  onAddToCart: () => void;
}

const ProductCard: React.FC<ProductCardProps> = ({
  name,
  price,
  country_of_origin,
  description,
  fruit_or_vegetable,
  expiry_date,
  imageUrl,
  onAddToCart,
}) => {
  return (
    <Card>
      <CardMedia
        component="img"
        height="140"
        image={imageUrl || "https://via.placeholder.com/150"}
        alt={name}
      />
      <CardContent>
        <Typography variant="h5" component="div">
          {name}
        </Typography>
        <Typography variant="body2" color="text.secondary">
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
        <Button className="add-to-cart" onClick={onAddToCart} variant="contained" color="primary">
          Dodaj do koszyka
        </Button>
      </CardContent>
    </Card>
  );
};

export default ProductCard;
