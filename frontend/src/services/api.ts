import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
});

export const searchCVEs = async (
  query: string,
  filters: Record<string, any> = {}
) => {
  const payload: any = { query };

  if (Object.keys(filters).length > 0) {
    payload.filters = filters;
  }

  const response = await api.post('/search', payload);
  return response.data;
};

export const getCVEDetail = async (id: string) => {
  const response = await api.get(`/cve/${id}`);
  return response.data;
};

export const askCyberRAG = async (
  query: string,
  filters: Record<string, any> = {}
) => {
  const payload: any = { query };

  if (Object.keys(filters).length > 0) {
    payload.filters = filters;
  }

  const response = await api.post('/ask', payload);
  return response.data;
};
