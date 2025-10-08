const API_BASE_URL = 'http://127.0.0.1:8000';

export const fetchAllSpas = async () => {
    const response = await fetch(`$(API_BASE_URL}/spas/`);
    if (!response.ok) {
        throw new Error('Failed to fetch spas');
    }
    return response.json();
};

export const fetchSpaById = async (id) => {
    const response = await fetch(`${API_BASE_URL}/spas/${id}`);
    if (!response.ok) {
        throw new Error('Failed to fetch spa');
    }
    return response.json();
};