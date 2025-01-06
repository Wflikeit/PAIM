import { createSlice, PayloadAction } from "@reduxjs/toolkit";

interface CartItem {
    id: string;
    name: string;
    price: number;
    quantity: number;
}

interface CartState {
    items: CartItem[];
}

const initialState: CartState = {
    items: [],
};

const cartSlice = createSlice({
    name: "cart",
    initialState,
    reducers: {
        addToCart: (state, action: PayloadAction<CartItem>) => {
            console.log("Before adding item:", JSON.parse(JSON.stringify(state.items))); // Convert Proxy to plain array
            const existingItem = state.items.find((item) => item.id === action.payload.id);
            if (existingItem) {
                console.log("Item exists, incrementing quantity"); // Debugging log
                existingItem.quantity += 1;
            } else {
                console.log("Adding new item to cart"); // Debugging log
                state.items.push({ ...action.payload, quantity: 1 });
            }
            console.log("After adding item:", JSON.parse(JSON.stringify(state.items))); // Convert Proxy to plain array
        },



        removeFromCart: (state, action: PayloadAction<string>) => {
            state.items = state.items.filter((item) => item.id !== action.payload);
        },
        clearCart: (state) => {
            state.items = [];
        },
    },
});

export const { addToCart, removeFromCart, clearCart } = cartSlice.actions;
export default cartSlice.reducer;
