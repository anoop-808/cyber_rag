import React, { useState } from 'react';
import { ChatIcon } from './icons';

interface AskFormProps {
    onAsk: (query: string) => void;
    loading: boolean;
}

const EXAMPLE_QUESTIONS = [
    'Explain CVE-2021-44228',
    'What is SQL Injection?',
    'Show critical Apache vulnerabilities',
    'Buffer overflow examples',
];

const MAX_LENGTH = 500;

const AskForm: React.FC<AskFormProps> = ({ onAsk, loading }) => {
    const [query, setQuery] = useState('');

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        const trimmed = query.trim();
        if (trimmed && !loading) {
            onAsk(trimmed);
        }
    };

    return (
        <form className="ask-form" role="search" onSubmit={handleSubmit}>
            <div className="ask-card">
                <textarea
                    name="question"
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    placeholder="Ask CyberRAG anything about CVEs, exploits, or security best practices..."
                    maxLength={MAX_LENGTH}
                    disabled={loading}
                    rows={3}
                    aria-label="Ask a cybersecurity question"
                />

                <div className="ask-examples">
                    <span className="ask-examples-label">Example questions</span>
                    <div className="ask-example-list">
                        {EXAMPLE_QUESTIONS.map((question) => (
                            <button
                                key={question}
                                type="button"
                                className="ask-example-chip"
                                onClick={() => setQuery(question)}
                                disabled={loading}
                            >
                                {question}
                            </button>
                        ))}
                    </div>
                </div>

                <div className="ask-form-footer">
                    <span
                        className={`char-counter${query.length >= MAX_LENGTH ? ' near-limit' : ''}`}
                        aria-live="polite"
                    >
                        {query.length}/{MAX_LENGTH}
                    </span>
                    <button type="submit" className="btn btn-primary" disabled={loading || !query.trim()}>
                        {loading ? (
                            <>
                                <span className="btn-spinner" aria-hidden="true" />
                                Analyzing...
                            </>
                        ) : (
                            <>
                                <ChatIcon />
                                Ask
                            </>
                        )}
                    </button>
                </div>
            </div>
        </form>
    );
};

export default AskForm;
