import React, { useState } from 'react';
import SeverityFilter from './SeverityFilter';
import { SearchIcon } from './icons';

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
        <form className="search-bar" role="search" onSubmit={handleSubmit}>
            <div className="search-input-wrap">
                <span className="search-input-icon">
                    <SearchIcon />
                </span>
                <input
                    type="text"
                    name="query"
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    placeholder="Search vulnerabilities, vendors, or products..."
                    disabled={loading}
                    aria-label="Search vulnerabilities"
                />
            </div>
            <SeverityFilter value={severity} onChange={setSeverity} disabled={loading} />
            <button type="submit" className="btn btn-primary" disabled={loading || !query.trim()}>
                {loading ? 'Searching...' : 'Search'}
            </button>
        </form>
    );
}
export default SearchBar;
