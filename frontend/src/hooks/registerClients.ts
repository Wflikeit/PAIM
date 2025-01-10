import axios, { AxiosError } from "axios";

interface Client {
  email: string;
  payment_address: string;
  delivery_address: string;
  nip: string;
  password: string;
  company_name: string;
}

const registerClients = () => {
  const addClient = async (clientData: Client): Promise<void> => {
    const clientdata = JSON.stringify(clientData);

    try {
      const response = await axios.post(
        "http://localhost:8002/api/register",
        clientdata,
        {
          headers: {
            "Content-Type": "application/json",
          },
        },
      );
      console.log("Client registered successfully:", response.data);
    } catch (error) {
      if (error instanceof AxiosError) {
        console.error("Error response data:", error.response?.data);
        console.error("Error response status:", error.response?.status);
        console.error("Error response headers:", error.response?.headers);
      } else {
        console.error("Failed to register client:", error);
      }
      throw new Error("Could not register client");
    }
  };

  return { addClient };
};

export default registerClients;