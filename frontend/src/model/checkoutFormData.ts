import { createSlice, PayloadAction } from "@reduxjs/toolkit";

// Checkout form data model
export interface CheckoutFormModel {
  voivodeship: string;
  city: string;
  street: string; // Changed to string, as street names are not numbers
  houseNumber: string; // Changed to string to accommodate formats like "12A"
  postalCode: string;
  deliveryDate: Date;
}

// State for storing checkout form data
interface CheckoutState {
  formData: CheckoutFormModel | null; // Store the form data or null when cleared
}

const initialState: CheckoutState = {
  formData: null, // Initialize with no data
};

const checkoutSlice = createSlice({
  name: "checkout",
  initialState,
  reducers: {
    // Add or update checkout form data
    updateCheckoutFormData: (
      state,
      action: PayloadAction<CheckoutFormModel>,
    ) => {
      state.formData = action.payload; // Replace the existing data with new data
    },

    // Clear the checkout form data
    clearCheckoutFormData: (state) => {
      state.formData = null; // Reset the form data
    },
  },
});

// Export actions and reducer
export const { updateCheckoutFormData, clearCheckoutFormData } =
  checkoutSlice.actions;
export default checkoutSlice.reducer;
