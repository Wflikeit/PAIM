import { configureStore } from "@reduxjs/toolkit";
import { persistReducer, persistStore } from "redux-persist";
import storage from "redux-persist/lib/storage"; // Use localStorage as default
import productsReducer from "../model/product";
import cartReducer from "../model/cardItem";
import checkoutFormDataReducer from "../model/checkoutFormData";
import orderReducer from "../model/order";

const persistConfig = {
  key: "root",
  storage,
};

const persistedCartReducer = persistReducer(persistConfig, cartReducer);
const persistedCheckoutFormDataReducer = persistReducer(
  persistConfig,
  checkoutFormDataReducer,
);
const persistedOrderReducer = persistReducer(persistConfig, orderReducer);

const store = configureStore({
  reducer: {
    cart: persistedCartReducer,
    products: productsReducer,
    checkoutFormData: persistedCheckoutFormDataReducer,
    order: persistedOrderReducer,
  },
});

export const persistor = persistStore(store);
export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;

export default store;