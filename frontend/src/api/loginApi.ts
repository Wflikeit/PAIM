import axios from "axios";

const login = async (email, password) => {
    try {
        const response = await axios.post("http://127.0.0.1:8000/admin/login", {
            username: email,
            password: password
        });
        localStorage.setItem("token", response.data.access_token);
        return response.data;
    } catch (error) {
        console.error("Login failed", error);
        throw error;
    }
};
