import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || '',
  headers: {
    'Content-Type': 'application/json',
  },
});

export const searchAPI = async (query: string) => {
  const response = await api.post('/search', { query });
  return response.data;
};

export const askAPI = async (query: string) => {
  const response = await api.post('/ask', { query });
  return response.data;
};

export const getCveAPI = async (id: string) => {
  const response = await api.get(`/cve/${id}`);
  return response.data;
};

export default api;
