import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { getCVEDetail } from '../services/api';
import { LoadingState, ErrorState } from './ui';
import SeverityBadge from './SeverityBadge';
import { CheckIcon, CopyIcon, ExternalLinkIcon, ChatIcon, StarIcon } from './icons';
import { useFavorites } from '../hooks/useFavorites';
import { useRecentlyViewed } from '../hooks/useRecentlyViewed';
import { formatDate, copyToClipboard, severityLevel, cvssPercent } from '../utils/format';
import { useToast } from './ui/toast-context';

interface CVEDetailProps {
    cveId: string;
    onBack: () => void;
}

function CVEInfoCard({ cveId, onBack }: CVEDetailProps) {
    const [cve, setCve] = useState<any>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [retryKey, setRetryKey] = useState(0);
    const [copied, setCopied] = useState(false);
    const { showToast } = useToast();
    const { favorites, toggleFavorite } = useFavorites();
    const isFavorite = favorites.includes(cveId);
    const { addViewed } = useRecentlyViewed();

    useEffect(() => {
        const fetchDetail = async () => {
            setLoading(true);
            setError(null);
            setCopied(false);
            try {
                const data = await getCVEDetail(cveId);
                setCve(data);
                // Record the open (deduped to the front) — re-fires on retry, which is intentional.
                addViewed(cveId);
            } catch {
                setError('Failed to fetch CVE details. Please try again.');
            } finally {
                setLoading(false);
            }
        };

        if (cveId) {
            fetchDetail();
        }
    }, [cveId, retryKey, addViewed]);

    const handleCopy = async () => {
        const ok = await copyToClipboard(cve?.id ?? cveId);
        if (ok) {
            setCopied(true);
            showToast('CVE ID copied');
            window.setTimeout(() => setCopied(false), 2000);
        }
    };

    if (loading) return <LoadingState label="Loading CVE..." skeleton />;
    if (error) return <ErrorState message={error} onRetry={() => setRetryKey((k) => k + 1)} />;
    if (!cve) return null;

    const level = severityLevel(cve.severity);
    const cvssScore = cve.cvss?.score;
    const hasCvss = cvssScore !== null && cvssScore !== undefined && !Number.isNaN(Number(cvssScore));
    const cvssPercentValue = cvssPercent(cvssScore) ?? 0;
    const published = formatDate(cve.published);
    const modified = formatDate(cve.modified);

    // Group CPEs into unique vendor/product entries with their versions.
    const productMap: Record<string, { vendor: string; product: string; versions: Set<string> }> = {};
    (cve.cpes || []).forEach((cpe: any) => {
        const vendor = cpe.vendor || 'Unknown';
        const product = cpe.product || cpe.uri || 'Unknown';
        const key = `${vendor}::${product}`;
        if (!productMap[key]) {
            productMap[key] = { vendor, product, versions: new Set() };
        }
        if (cpe.version) {
            productMap[key].versions.add(cpe.version);
        }
    });
    const products = Object.values(productMap);

    const referenceUrl = (ref: any): string | null => {
        if (typeof ref === 'string') return ref || null;
        return ref?.url || null;
    };

    return (
        <div className="cve-detail-container">
            <div className="cve-detail-topbar">
                <button className="back-button" onClick={onBack}>&larr; Back to Results</button>
                <button
                    type="button"
                    className={`btn btn-ghost copy-button${copied ? ' copied' : ''}`}
                    onClick={handleCopy}
                    aria-label={copied ? 'CVE ID copied' : 'Copy CVE ID'}
                >
                    {copied ? <CheckIcon /> : <CopyIcon />}
                    {copied ? 'Copied!' : 'Copy CVE ID'}
                </button>
            </div>

            <div className="cve-detail-header">
                <h2>{cve.id || 'Not Available'}</h2>
                <div className="cve-header-actions">
                    <button
                        type="button"
                        className={`star-btn${isFavorite ? ' starred' : ''}`}
                        onClick={() => toggleFavorite(cve.id)}
                        aria-pressed={isFavorite}
                        aria-label={isFavorite ? `Remove ${cve.id} from favorites` : `Add ${cve.id} to favorites`}
                    >
                        <StarIcon filled={isFavorite} />
                    </button>
                    <SeverityBadge severity={cve.severity} />
                </div>
            </div>

            <div className="cve-detail-meta-grid">
                <div className="meta-group">
                    <h4>Severity</h4>
                    <SeverityBadge severity={cve.severity} />
                </div>
                <div className="meta-group">
                    <h4>CVSS</h4>
                    {hasCvss ? (
                        <>
                            <span className={`cvss-score-text ${level}`}>{Number(cvssScore).toFixed(1)}</span>
                            <div className="cvss-meter" aria-hidden="true">
                                <div className={`cvss-meter-fill ${level}`} style={{ width: `${cvssPercentValue}%` }} />
                            </div>
                        </>
                    ) : (
                        <span>Not Available</span>
                    )}
                </div>
                <div className="meta-group">
                    <h4>Published</h4>
                    <span>{published || 'Not Available'}</span>
                </div>
                <div className="meta-group">
                    <h4>Updated</h4>
                    <span>{modified || 'Not Available'}</span>
                </div>
            </div>

            <div className="cve-detail-body">
                <section>
                    <h3>Overview</h3>
                    <p>{cve.description || 'Not Available'}</p>
                </section>

                <section>
                    <h3>Technical Details</h3>

                    {cve.cwe ? (
                        <div className="tech-detail-grid">
                            <div className="meta-group">
                                <h4>CWE</h4>
                                <span className="mono">{cve.cwe.id}</span>
                                {cve.cwe.name && <p className="tech-note">{cve.cwe.name}</p>}
                            </div>
                        </div>
                    ) : null}

                    {products.length > 0 ? (
                        <div className="products-block">
                            {products.map((entry) => (
                                <div className="tech-detail-grid" key={`${entry.vendor}::${entry.product}`}>
                                    <div className="meta-group">
                                        <h4>Vendor</h4>
                                        <span>{entry.vendor}</span>
                                    </div>
                                    <div className="meta-group">
                                        <h4>Product</h4>
                                        <span>{entry.product}</span>
                                    </div>
                                    <div className="meta-group">
                                        <h4>Affected Versions</h4>
                                        <span>{entry.versions.size > 0 ? [...entry.versions].join(', ') : 'Not Available'}</span>
                                    </div>
                                </div>
                            ))}
                        </div>
                    ) : (
                        <p className="tech-note">No affected products available.</p>
                    )}
                </section>

                <section>
                    <h3>References</h3>
                    {cve.references && cve.references.length > 0 ? (
                        <ul className="reference-list">
                            {cve.references.map((ref: any, index: number) => {
                                const url = referenceUrl(ref);
                                if (!url) return null;
                                return (
                                    <li key={index}>
                                        <a href={url} target="_blank" rel="noopener noreferrer">
                                            <span className="reference-url">{url}</span>
                                            <ExternalLinkIcon />
                                        </a>
                                    </li>
                                );
                            })}
                        </ul>
                    ) : (
                        <p className="tech-note">No external references available.</p>
                    )}
                </section>
            </div>

            <div className="cve-detail-actions">
                <Link to="/ask" className="btn btn-primary">
                    <ChatIcon />
                    Ask AI about this CVE
                </Link>
                <button type="button" className="btn btn-secondary copy-button" onClick={handleCopy}>
                    {copied ? <CheckIcon /> : <CopyIcon />}
                    {copied ? 'Copied!' : 'Copy CVE ID'}
                </button>
            </div>
        </div>
    );
}

export default CVEInfoCard;
