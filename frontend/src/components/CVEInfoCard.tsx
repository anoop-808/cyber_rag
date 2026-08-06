import React, { useState, useEffect } from 'react';
import { getCVEDetail } from '../services/api';

interface CVEDetailProps {
    cveId: string;
    onBack: () => void;
}

function CVEInfoCard({ cveId, onBack }: CVEDetailProps) {
    const [cve, setCve] = useState<any>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const fetchDetail = async () => {
            setLoading(true);
            setError(null);
            try {
                const data = await getCVEDetail(cveId);
                setCve(data);
            } catch (err) {
                setError('Failed to fetch CVE details.');
            } finally {
                setLoading(false);
            }
        };

        if (cveId) {
            fetchDetail();
        }
    }, [cveId]);

    if (loading) return <div className="loading-state"><p>Loading CVE...</p></div>;
    if (error) return <div className="error-state"><p>CVE not found.</p></div>;
    if (!cve) return null;

    return (
        <div className="cve-detail-container">
            <button className="back-button" onClick={onBack}>&larr; Back to Results</button>

            <div className="cve-detail-header">
                <h2>{cve.id || 'Not Available'}</h2>
            </div>

            <div className="cve-detail-meta-grid">
                <div className="meta-group">
                    <h4>Severity</h4>
                    <span className={`severity-badge ${cve.severity ? cve.severity.toLowerCase() : 'unknown'}`}>
                        {cve.severity || 'Not Available'}
                    </span>
                </div>
                <div className="meta-group">
                    <h4>CVSS</h4>
                    <span className="cvss-score">{cve.cvss?.score || 'Not Available'}</span>
                </div>
                <div className="meta-group">
                    <h4>Published</h4>
                    <span>{cve.published ? new Date(cve.published).toLocaleDateString() : 'Not Available'}</span>
                </div>
                <div className="meta-group">
                    <h4>Modified</h4>
                    <span>{cve.modified ? new Date(cve.modified).toLocaleDateString() : 'Not Available'}</span>
                </div>
            </div>

            <div className="cve-detail-body">
                <section>
                    <h3>Description</h3>
                    <p>{cve.description || 'Not Available'}</p>
                </section>

                <section>
                    <h3>CWE</h3>
                    {cve.cwe ? (
                        <p><strong>{cve.cwe.id}:</strong> {cve.cwe.name || 'Not Available'}</p>
                    ) : (
                        <p>Not Available</p>
                    )}
                </section>

                <section>
                    <h3>Affected Products (CPEs)</h3>
                    {cve.cpes && cve.cpes.length > 0 ? (
                        <ul className="cpe-list">
                            {cve.cpes.map((cpe) => (
                                <li key={cpe.id}>{cpe.uri}</li>
                            ))}
                        </ul>
                    ) : (
                        <p>Not Available</p>
                    )}
                </section>

                <section>
                    <h3>References</h3>
                    {cve.references && cve.references.length > 0 ? (
                        <ul className="reference-list">
                            {cve.references.map((ref, index) => {
                                // Handles both object structure {url: "..."} and string structure
                                const url = typeof ref === 'string' ? ref : ref.url;
                                if (!url) return null;
                                return (
                                    <li key={index}>
                                        <a href={url} target="_blank" rel="noopener noreferrer">{url}</a>
                                    </li>
                                );
                            })}
                        </ul>
                    ) : (
                        <p>Not Available</p>
                    )}
                </section>
            </div>
        </div>
    );
}

export default CVEInfoCard;
// Added for review visibility
