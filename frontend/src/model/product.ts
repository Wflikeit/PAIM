import { createAsyncThunk, createSlice, PayloadAction } from "@reduxjs/toolkit";
import { fetchProductsFromApi, Product } from "../api/productsApi";

interface ProductsState {
  products: Product[];
  filteredProducts: Product[];
  filters: {
    fruitOrVegetable: [];
    countryOfOrigin: []; // New filter
  };
  loading: boolean;
  error: string | null;
}

const initialState: ProductsState = {
  products: [],
  filteredProducts: [],
  filters: {
    fruitOrVegetable: [], // Initialize as an empty array
    countryOfOrigin: [], // Initialize as an empty array
  },
  loading: false,
  error: null,
};

// Async thunk to fetch products
export const fetchProducts = createAsyncThunk<Product[]>(
  "products/fetchProducts",
  async () => {
    return await fetchProductsFromApi();
  },
);

const toggleFilter = (currentFilters: string[], value: string): string[] => {
  return currentFilters.includes(value)
    ? currentFilters.filter((item) => item !== value) // Remove if exists
    : [...currentFilters, value]; // Add if not exists
};

const productsSlice = createSlice({
  name: "products",
  initialState,
  reducers: {
    applyFilter(state) {
      const { fruitOrVegetable, countryOfOrigin } = state.filters;

      state.filteredProducts = state.products.filter((product) => {
        const matchesFruitOrVegetable =
          fruitOrVegetable.length === 0 ||
          fruitOrVegetable.includes(product.fruit_or_vegetable);

        const matchesCountryOfOrigin =
          countryOfOrigin.length === 0 ||
          countryOfOrigin.includes(product.country_of_origin);

        return matchesFruitOrVegetable && matchesCountryOfOrigin;
      });
    },

    setFruitOrVegetableFilter(state, action: PayloadAction<string>) {
      state.filters.fruitOrVegetable = toggleFilter(
        state.filters.fruitOrVegetable,
        action.payload,
      );
    },
    setCountryOfOriginFilter(state, action: PayloadAction<string>) {
      state.filters.countryOfOrigin = toggleFilter(
        state.filters.countryOfOrigin,
        action.payload,
      );
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

export const {
  applyFilter,
  setFruitOrVegetableFilter,
  setCountryOfOriginFilter, // Export new action
} = productsSlice.actions;

export default productsSlice.reducer;