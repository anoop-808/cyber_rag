import React from 'react';
import SeverityBadge from './SeverityBadge';
import { useNavigate } from 'react-router-dom';
import '../styles/App.css';

interface SearchResultCardProps {
    cve: any; // We'll just use any for now, or define a better type if available
    onClick?: (id: string) => void;
}

const SearchResultCard: React.FC<SearchResultCardProps> = ({ cve, onClick }) => {
    const navigate = useNavigate();

    const handleClick = () => {
        if (onClick) {
            onClick(cve.id);
        } else {
            navigate(`/cve/${cve.id}`);
        }
    };

    // Assuming metadata contains severity, cvss, published_date etc. based on backend search response
    const metadata = cve.metadata || {};
    const severity = metadata.severity || cve.severity;
    const cvssScore = metadata.cvss_score || metadata.cvss || cve.cvss_score;
    const publishedDate = metadata.published_date || cve.published_date;
    const publishedYear = publishedDate ? new Date(publishedDate).getFullYear() : null;

    return (
        <div className="cve-card search-result-card" onClick={handleClick} style={{ cursor: 'pointer' }}>
            <div className="card-header">
                <h3>{cve.id}</h3>
            </div>

            <div className="card-body">
                <p>{cve.description}</p>
            </div>

            <div className="card-footer" style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap', alignItems: 'center', marginTop: '1rem' }}>
                <div className="meta-item">
                    <strong>Severity: </strong>
                    <SeverityBadge severity={severity} />
                </div>

                {cvssScore !== undefined && cvssScore !== null && (
                    <div className="meta-item">
                        <strong>CVSS: </strong> <span>{cvssScore}</span>
                    </div>
                )}

                {publishedYear && (
                    <div className="meta-item">
                        <strong>Published: </strong> <span>{publishedYear}</span>
                    </div>
                )}
            </div>
        </div>
    );
};

export default SearchResultCard;
