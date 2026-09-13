import axios from "axios";

const api = axios.create({
  baseURL: "http://127.0.0.1:8000",
});

export const uploadSonarImage = async (file) => {
  const formData = new FormData();
  formData.append("file", file);

  const response = await api.post("/upload", formData);

  return response.data;
};

export const detectSonarImage = async (fileId) => {
  const response = await api.get(`/detect/${fileId}`);

  return response.data;
};

export default api;