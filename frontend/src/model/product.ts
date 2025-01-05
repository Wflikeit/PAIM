import { createAsyncThunk, createSlice, PayloadAction } from "@reduxjs/toolkit";
import { fetchProductsFromApi, Product } from "../api/productsApi";

interface ProductsState {
  products: Product[];
  filteredProducts: Product[];
  filters: {
    fruitOrVegetable: string | null;
  };
  loading: boolean;
  error: string | null;
}

const initialState: ProductsState = {
  products: [],
  filteredProducts: [],
  filters: {
    fruitOrVegetable: null,
  },
  loading: false,
  error: null,
};

// Async thunk to fetch products
export const fetchProducts = createAsyncThunk<Product[]>(
  "products/fetchProducts",
  async () => {
    const products = await fetchProductsFromApi();
    return products;
  },
);

const productsSlice = createSlice({
  name: "products",
  initialState,
  reducers: {
    applyFilter(state) {
      const { fruitOrVegetable } = state.filters;
      state.filteredProducts = state.products.filter((product) =>
        fruitOrVegetable
          ? product.fruit_or_vegetable === fruitOrVegetable
          : true,
      );
    },
    setFruitOrVegetableFilter(state, action: PayloadAction<string | null>) {
      state.filters.fruitOrVegetable = action.payload;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchProducts.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(
        fetchProducts.fulfilled,
        (state, action: PayloadAction<Product[]>) => {
          state.products = action.payload;
          state.filteredProducts = action.payload; // Initialize filtered products
          state.loading = false;
        },
      )
      .addCase(fetchProducts.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message || "Failed to load products";
      });
  },
});

export const { applyFilter, setFruitOrVegetableFilter } = productsSlice.actions;

export default productsSlice.reducer;