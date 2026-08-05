import axios from 'axios';

export const searchCVEs = async (query: string, filters: Record<string, any> = {}) => {
    const payload: any = { query };
    if (Object.keys(filters).length > 0) {
        payload.filters = filters;
    }
    const response = await axios.post(`/search`, payload);
    return response.data;
};

export const getCVEDetail = async (id: string) => {
    const response = await axios.get(`/cve/${id}`);
    return response.data;
};
