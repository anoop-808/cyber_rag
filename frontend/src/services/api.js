import axios from 'axios';

export const searchCVEs = async (query) => {
    const response = await axios.get(`/search`, {
        params: { query }
    });
    return response.data;
};
