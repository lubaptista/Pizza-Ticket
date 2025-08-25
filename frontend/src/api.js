import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:5000",
});

// Intercepta cada request e adiciona o token se existir
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("token"); // ou sessionStorage
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Intercepta responses para tratar erros globais
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      console.warn("Não autorizado, talvez o token tenha expirado.");
      // Aqui você pode redirecionar para login, por exemplo
    }
    return Promise.reject(error);
  }
);

export default api;
