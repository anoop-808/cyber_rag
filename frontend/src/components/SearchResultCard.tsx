import React from 'react';
import SeverityBadge from './SeverityBadge';
import { useNavigate } from 'react-router-dom';
import { StarIcon } from './icons';
import { useFavorites } from '../hooks/useFavorites';
import { formatDate, severityLevel, cvssPercent } from '../utils/format';
import '../styles/App.css';

interface SearchResultCardProps {
    cve: any; // Backend document shape: { id, description, severity?, cwe_id?, metadata: {...} }
    onClick?: (id: string) => void;
}

const SearchResultCard: React.FC<SearchResultCardProps> = ({ cve, onClick }) => {
    const navigate = useNavigate();
    const { favorites, toggleFavorite } = useFavorites();
    const isFavorite = favorites.includes(cve.id);

    const handleClick = () => {
        if (onClick) {
            onClick(cve.id);
        } else {
            navigate(`/cve/${cve.id}`);
        }
    };

    const handleKeyDown = (e: React.KeyboardEvent) => {
        if (e.key === 'Enter' || e.key === ' ') {
            e.preventDefault();
            handleClick();
        }
    };

    const metadata = cve.metadata || {};
    const severity = metadata.severity || cve.severity;
    const level = severityLevel(severity);
    const cvssScore = metadata.cvss_score ?? metadata.cvss ?? cve.cvss_score;
    const hasCvss = cvssScore !== undefined && cvssScore !== null && !Number.isNaN(Number(cvssScore));
    const rawPublished = metadata.published ?? cve.published ?? cve.published_date;
    const rawModified = metadata.last_modified ?? cve.modified;
    const published = formatDate(rawPublished);
    const lastModified = formatDate(rawModified);
    const cweId = cve.cwe_id || metadata.cwe_id;

    return (
        <div className="cve-card search-result-card" onClick={handleClick} role="button" tabIndex={0} onKeyDown={handleKeyDown}>
            <div className="card-header">
                <h3 className="cve-id">{cve.id}</h3>
                <div className="card-header-actions">
                    <button
                        type="button"
                        className={`star-btn${isFavorite ? ' starred' : ''}`}
                        onClick={(e) => {
                            e.stopPropagation();
                            toggleFavorite(cve.id);
                        }}
                        onKeyDown={(e) => e.stopPropagation()}
                        aria-pressed={isFavorite}
                        aria-label={isFavorite ? `Remove ${cve.id} from favorites` : `Add ${cve.id} to favorites`}
                    >
                        <StarIcon filled={isFavorite} />
                    </button>
                    <SeverityBadge severity={severity} />
                </div>
            </div>

            {hasCvss && (
                <div className="cvss-row" aria-label={`CVSS score ${Number(cvssScore).toFixed(1)} out of 10`}>
                    <span className="cvss-label">CVSS</span>
                    <div className="cvss-meter" aria-hidden="true">
                        <div className={`cvss-meter-fill ${level}`} style={{ width: `${cvssPercent(cvssScore)}%` }} />
                    </div>
                    <span className={`cvss-score-text ${level}`}>{Number(cvssScore).toFixed(1)}</span>
                </div>
            )}

            <p className="card-description">{cve.description}</p>

            <div className="card-footer">
                {published && (
                    <span className="meta-item">
                        <span className="meta-label">Published</span>
                        <time dateTime={rawPublished || undefined}>{published}</time>
                    </span>
                )}
                {lastModified && (
                    <span className="meta-item">
                        <span className="meta-label">Modified</span>
                        <time dateTime={rawModified || undefined}>{lastModified}</time>
                    </span>
                )}
                {cweId && (
                    <span className="meta-item">
                        <span className="meta-label">CWE</span>
                        <span className="mono">{cweId}</span>
                    </span>
                )}
            </div>
        </div>
    );
};

export default SearchResultCard;
