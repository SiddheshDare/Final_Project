import axios from "axios";

// Use relative URL in production or environment variable
const BASE_URL = process.env.NODE_ENV === 'production' 
  ? '/api' 
  : "http://127.0.0.1:8000";

export const trainModel = async () => {
  try {
    const response = await axios.get(`${BASE_URL}/training/`);
    return response.data;
  } catch (error) {
    console.error("Error during training:", error);
    return null;
  }
};

export const predictAttrition = async (features) => {
  try {
    const response = await axios.post(`${BASE_URL}/prediction/`, features);
    return response.data;
  } catch (error) {
    console.error("Error during prediction:", error);
    return null;
  }
};