import React from 'react';
import CVECard from './CVECard';

interface SearchResultsProps {
    results: any[];
    loading: boolean;
    error: string | null;
    hasSearched: boolean;
    onCveClick: (id: string) => void;
}

function SearchResults({ results, loading, error, hasSearched, onCveClick }: SearchResultsProps) {
    if (loading) return <div className="loading">Loading...</div>;
    if (error) return <div className="error">{error}</div>;

    if (hasSearched && results.length === 0) {
        return <div className="no-results">No results found.</div>;
    }

    return (
        <div className="search-results">
            {results.map((cve) => (
                <CVECard key={cve.id} cve={cve} onClick={onCveClick} />
            ))}
        </div>
    );
}
export default SearchResults;
