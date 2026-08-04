import React from 'react';

function CVECard({ cve, onClick }) {
    return (
        <div className="cve-card" style={{ cursor: 'pointer' }} onClick={() => onClick && onClick(cve.id)}>
            <div className="cve-card-header">
                <h3>{cve.id}</h3>
                <span className={`severity-badge ${cve.severity ? cve.severity.toLowerCase() : 'unknown'}`}>
                    {cve.severity || 'UNKNOWN'}
                </span>
            </div>
            <p className="cve-card-desc">{cve.description}</p>
            {cve.cwe_id && <p className="cwe">{cve.cwe_id}</p>}
        </div>
    );
}
export default CVECard;
