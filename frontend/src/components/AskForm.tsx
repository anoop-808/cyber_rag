import React, { useState } from 'react';

interface AskFormProps {
    onAsk: (query: string) => void;
    loading: boolean;
}

const AskForm: React.FC<AskFormProps> = ({ onAsk, loading }) => {
    const [query, setQuery] = useState('');

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if (query.trim() && !loading) {
            onAsk(query.trim());
        }
    };

    return (
        <form className="ask-form search-bar" onSubmit={handleSubmit}>
            <input
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Ask CyberRAG anything about CVEs."
                disabled={loading}
            />
            <button type="submit" disabled={loading || !query.trim()}>
                {loading ? 'Generating answer...' : 'Ask'}
            </button>
        </form>
    );
};

export default AskForm;
