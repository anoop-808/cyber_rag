import React, { useState } from 'react';
import SeverityFilter from './SeverityFilter';

interface SearchBarProps {
    onSearch: (query: string, filters: Record<string, any>) => void;
    initialQuery?: string;
    loading?: boolean;
}

function SearchBar({ onSearch, initialQuery = '', loading = false }: SearchBarProps) {
    const [query, setQuery] = useState(initialQuery);
    const [severity, setSeverity] = useState('');

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if (query.trim() && !loading) {
            const filters: Record<string, any> = {};
            if (severity) {
                filters.severity = severity;
            }
            onSearch(query.trim(), filters);
        }
    };

    return (
        <form className="search-bar" onSubmit={handleSubmit}>
            <input
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Search vulnerabilities........"
                disabled={loading}
            />
            <SeverityFilter value={severity} onChange={setSeverity} disabled={loading} />
            <button type="submit" disabled={loading || !query.trim()}>
                {loading ? 'Searching...' : 'Search'}
            </button>
        </form>
    );
}
export default SearchBar;
