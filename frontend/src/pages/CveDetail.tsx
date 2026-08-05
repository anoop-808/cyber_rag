import React from 'react';
import { useParams } from 'react-router-dom';

const CveDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>();

  return (
    <div>
      <h1>CVE Detail</h1>
      <p>Viewing details for {id}</p>
    </div>
  );
};

export default CveDetail;
