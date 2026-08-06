import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import AnswerText from './AnswerText';
import SeverityBadge from './SeverityBadge';
import { CheckIcon, CopyIcon, ExternalLinkIcon } from './icons';
import { copyToClipboard } from '../utils/format';
import { useToast } from './ui/toast-context';

interface AnswerCardProps {
    answer: string;
    sources: string[];
    metadata?: Record<string, any>[];
    confidence: number | null;
}

const AnswerCard: React.FC<AnswerCardProps> = ({ answer, sources, metadata = [], confidence }) => {
    const { showToast } = useToast();
    const [copied, setCopied] = useState(false);

    const handleCopy = async () => {
        const ok = await copyToClipboard(answer);
        if (ok) {
            setCopied(true);
            showToast('Answer copied to clipboard');
            window.setTimeout(() => setCopied(false), 2000);
        }
    };

    const metaById = new Map(metadata.map((meta) => [meta.id, meta]));
    const hasConfidence = confidence !== null && confidence !== undefined && !Number.isNaN(Number(confidence));
    const confidencePct = hasConfidence ? Math.min(100, Math.max(0, Number(confidence) * 100)) : 0;

    return (
        <div className="answer-card">
            <div className="answer-card-header">
                <h3>Analysis</h3>
                <button
                    type="button"
                    className="btn btn-ghost copy-answer-btn"
                    onClick={handleCopy}
                    aria-label={copied ? 'Answer copied' : 'Copy entire answer'}
                >
                    {copied ? <CheckIcon /> : <CopyIcon />}
                    {copied ? 'Copied' : 'Copy answer'}
                </button>
            </div>

            <div className="answer-prose">
                <AnswerText text={answer} />
            </div>

            {hasConfidence && (
                <div className="confidence-section">
                    <div className="confidence-header">
                        <span className="section-label">Confidence</span>
                        <span className="confidence-value">{Math.round(confidencePct)}%</span>
                    </div>
                    <div className="confidence-bar" aria-hidden="true">
                        <div className="confidence-bar-fill" style={{ width: `${confidencePct}%` }} />
                    </div>
                </div>
            )}

            {sources.length > 0 && (
                <div className="answer-sources">
                    <h3>Sources</h3>
                    <div className="source-grid">
                        {sources.map((id) => {
                            const meta = metaById.get(id);
                            const isCve = /^CVE-\d/i.test(id);
                            const content = (
                                <>
                                    <span className="source-title mono">{id}</span>
                                    <span className="source-type">CVE Record</span>
                                    <span className="source-meta">
                                        {meta?.severity && <SeverityBadge severity={meta.severity} />}
                                        {meta?.cvss !== undefined && meta?.cvss !== null && (
                                            <span className="source-cvss">CVSS {Number(meta.cvss).toFixed(1)}</span>
                                        )}
                                    </span>
                                </>
                            );

                            return isCve ? (
                                <Link to={`/cve/${id}`} className="source-card" key={id}>
                                    {content}
                                </Link>
                            ) : (
                                <a href={id} target="_blank" rel="noopener noreferrer" className="source-card" key={id}>
                                    {content}
                                    <ExternalLinkIcon />
                                </a>
                            );
                        })}
                    </div>
                </div>
            )}
        </div>
    );
};

export default AnswerCard;
