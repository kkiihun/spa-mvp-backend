import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { fetchAllSpas } from '../services/api';

const SpaList = () => {
    const [spas, setSpas] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const getSpas = async () => {
            try {
                const data = await fetchAllSpas();
                setSpas(data);
            } catch (err) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        };
        getSpas();
    }, []);

    if (loading) return <div className="text-center mt-8">로딩 중...</div>;
    if (error) return <div className="text-center mt-8 text-red-500">에러: {error}</div>;

    return (
        <div className="container mx-auto p-4">
            <h1 className="text-3xl font-bold text-center mb-8">국내 온천 목록</h1>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {spas.map(spa => (
                    <div key={spa.id} className="bg-white rounded-lg shadow-lg p-6">
                        <h2 className="text-xl font-semibold mb-2">{spa.name}</h2>
                        <p className="text-gray-600 mb-2">{spa.address}</p>
                        <Link to={`/spa/${spa.id}`} className="text-blue-500 hover:underline">
                            자세히 보기
                        </Link>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default SpaList;