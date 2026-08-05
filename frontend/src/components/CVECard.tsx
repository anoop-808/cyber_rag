import React from 'react';

export interface CVEData {
  id: string;
  severity?: string;
  description?: string;
  cwe_id?: string;
  [key: string]: any;
}

interface CVECardProps {
  cve: CVEData;
  onClick?: (id: string) => void;
}

const CVECard: React.FC<CVECardProps> = ({ cve, onClick }) => {
    return (
        <div className="cve-card" style={{ cursor: 'pointer' }} onClick={() => onClick && onClick(cve.id)}>
            <h3>{cve.id}</h3>
            <p className={`severity ${cve.severity ? cve.severity.toLowerCase() : 'unknown'}`}>
                {cve.severity || 'UNKNOWN'}
            </p>
            <p>{cve.description}</p>
            {cve.cwe_id && <p className="cwe">{cve.cwe_id}</p>}
        </div>
    );
}
export default CVECard;
