import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
console.log('Configured API Base URL:', API_BASE_URL);
const API_KEY = process.env.NEXT_PUBLIC_API_KEY || 'local-dev-key'; // Default for dev, should be set in env

const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'X-API-Key': API_KEY,
    },
});

export const uploadDocument = async (file: File) => {
    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await api.post('/upload', formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        });
        return response.data;
    } catch (error) {
        console.error('Error uploading document:', error);
        throw error;
    }
};

export const queryDocument = async (query: string) => {
    try {
        const response = await api.post('/api/generate', { query });
        return response.data;
    } catch (error) {
        console.error('Error querying document:', error);
        throw error;
    }
};

export default api;
