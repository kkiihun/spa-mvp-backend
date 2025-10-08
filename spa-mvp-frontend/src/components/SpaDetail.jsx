import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { fetchSpaById } from '../services/api';

const SpaDetail = () => {
  const { id } = useParams();
  const [spa, setSpa] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  console.log('1. 컴포넌트가 렌더링될 때 ID:', id);

  useEffect(() => {
    // URL 파라미터 id가 유효하지 않으면 API 호출을 중단합니다.
    if (!id) {
      setError('유효하지 않은 페이지입니다.');
      setLoading(false);
      return;
    }

    console.log('2. useEffect가 실행될 때 API 호출 시작');

    const getSpa = async () => {
      try {
        console.log(`3. fetchSpaById 함수 호출 중 (ID: ${id})`);
        const data = await fetchSpaById(id);
        console.log('4. API 호출 성공, 받은 데이터:', data);

        if (!data) {
          setError('해당하는 데이터가 없습니다.');
        } else {
          setSpa(data);
        }
      } catch (err) {
        // 네트워크 오류 등 API 호출 실패 시
        console.error('5. API 호출 실패, 에러 발생:', err);
        setError('데이터를 불러오는 데 실패했습니다. 잠시 후 다시 시도해 주세요.');
      } finally {
        setLoading(false);
        console.log('6. 로딩 상태 종료');
      }
    };
    getSpa();
  }, [id]);

  if (loading) return <div className="text-center mt-8">로딩 중...</div>;
  if (error) return <div className="text-center mt-8 text-red-500">에러: {error}</div>;

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-3xl font-bold mb-4">{spa.name}</h1>
      <img src={spa.image_url} alt={spa.name} className="w-full rounded-lg mb-4" />
      <div className="bg-white rounded-lg shadow-lg p-6">
        <p><strong>주소:</strong> {spa.address}</p>
        <p><strong>운영 시간:</strong> {spa.operating_hours}</p>
        <p><strong>이용 요금:</strong> {spa.price}</p>
        <p><strong>전화번호:</strong> {spa.phone_number}</p>
        <p className="mt-4">{spa.description}</p>
      </div>
    </div>
  );
};

export default SpaDetail;