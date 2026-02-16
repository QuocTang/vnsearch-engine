import axios from "axios";

/**
 * HTTP Client wrapper cho Axios
 * - Tự động thêm base URL từ env
 * - Interceptors cho auth và error handling
 */

// Tạo axios instance với config mặc định
const client = axios.create({
  timeout: 30000,
  headers: {
    "Content-Type": "application/json",
  },
});

// Request interceptor - thêm auth token nếu có
client.interceptors.request.use(
  (config) => {
    // Thêm Auth Token nếu cần (ví dụ: Bearer token)
    // const token = localStorage.getItem('token');
    // if (token) {
    //   config.headers.Authorization = `Bearer ${token}`;
    // }

    return config;
  },
  (error) => {
    return Promise.reject(error);
  },
);

// Response interceptor - xử lý response và errors
client.interceptors.response.use(
  (response) => {
    // Trả về data trực tiếp
    return response;
  },
  (error) => {
    // Global error handling
    if (error.response) {
      // Server responded với status code ngoài 2xx
      switch (error.response.status) {
        case 401:
          // Unauthorized - có thể redirect to login
          console.error("Unauthorized - Please login");
          break;
        case 403:
          // Forbidden
          console.error("Access forbidden");
          break;
        case 404:
          // Not found
          console.error("Resource not found");
          break;
        case 500:
          // Server error
          console.error("Server error");
          break;
        default:
          console.error("API Error:", error.response.status);
      }
    } else if (error.request) {
      // Request made nhưng không nhận được response
      console.error("No response from server");
    } else {
      // Lỗi khi setup request
      console.error("Request setup error:", error.message);
    }

    return Promise.reject(error);
  },
);

export const HttpClient = client;
