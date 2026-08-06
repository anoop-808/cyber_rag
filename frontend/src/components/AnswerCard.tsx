import React from 'react';
import { Link } from 'react-router-dom';
import '../styles/App.css'; // Adjust import path if needed

interface AnswerCardProps {
    answer: string;
    sources: string[];
    confidence: number | null;
}

const AnswerCard: React.FC<AnswerCardProps> = ({ answer, sources, confidence }) => {
    return (
        <div className="answer-card" style={{ marginTop: '2rem', padding: '1rem', border: '1px solid #ccc', borderRadius: '4px' }}>
            <div className="answer-section">
                <h3>Answer</h3>
                <p>{answer}</p>
            </div>

            {sources && sources.length > 0 && (
                <div className="sources-section" style={{ marginTop: '1.5rem' }}>
                    <h3>Sources</h3>
                    <ul>
                        {sources.map((source, index) => (
                            <li key={index}>
                                <Link to={`/cve/${source}`}>{source}</Link>
                            </li>
                        ))}
                    </ul>
                </div>
            )}

            <div className="confidence-section" style={{ marginTop: '1.5rem' }}>
                <h3>Confidence</h3>
                <p>{confidence !== null && confidence !== undefined ? confidence : 'Unknown'}</p>
            </div>
        </div>
    );
};

export default AnswerCard;
