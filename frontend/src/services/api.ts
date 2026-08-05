import axios from 'axios';

export const searchCVEs = async (query: string) => {
    const response = await axios.get(`/search`, {
        params: { query }
    });
    return response.data;
};

export const getCVEDetail = async (id: string) => {
    const response = await axios.get(`/cve/${id}`);
    return response.data;
};
