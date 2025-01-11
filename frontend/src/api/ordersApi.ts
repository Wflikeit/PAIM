import axios from "axios";
import { BACKEND_URL } from "../hooks/useProducts.ts";
import { useQuery } from "react-query";

export interface OrderReportItem {
  region: string;
  amount: number;
  order_count: number;
}

export const placeOrder = (orderDetails: any) => {
  return axios.post(BACKEND_URL + "/api/order", orderDetails);
};

export const getReportOfOrders = async (startDate: Date, endDate: Date) => {
  const response = await axios.get<OrderReportItem[]>( // <-- let axios know it's an array of OrderReportItem
    BACKEND_URL + "/api/orders/stats",
    {
      params: {
        start_date: startDate.toISOString(),
        end_date: endDate.toISOString(),
      },
    },
  );
  return response.data;
};

export const useGetOrders = (startDate: Date | null, endDate: Date | null) => {
  return useQuery<OrderReportItem[]>( // <-- the query returns an array of OrderReportItem
    ["orders", startDate?.toISOString(), endDate?.toISOString()],
    () => {
      if (!startDate || !endDate) {
        // Return an empty array if the user hasn't picked both dates
        return Promise.resolve([]);
      }
      return getReportOfOrders(startDate, endDate);
    },
    {
      // Only run this query if both dates are set
      enabled: !!startDate && !!endDate,
      staleTime: 1000 * 60, // 1 minute
      refetchOnWindowFocus: false,
    },
  );
};