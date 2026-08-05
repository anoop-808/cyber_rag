import React from 'react';

interface CVECardProps {
    cve: any;
    onClick?: (id: string) => void;
}

function CVECard({ cve, onClick }: CVECardProps) {
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
