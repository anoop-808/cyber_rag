import axios from 'axios';

export const searchCVEs = async (query) => {
    const response = await axios.get(`/search`, {
        params: { query }
    });
    return response.data;
};

export const getCVEDetail = async (id) => {
    const response = await axios.get(`/cve/${id}`);
    return response.data;
};
