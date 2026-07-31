import React from 'react';
import CVECard from './CVECard';

function SearchResults({ results, loading, error, hasSearched, onCveClick }) {
    if (loading) return <div className="loading">Loading...</div>;
    if (error) return <div className="error">{error}</div>;

    if (hasSearched && results.length === 0) {
        return (
            <div className="no-results-state">
                <h3>No matching CVEs found</h3>
                <p>Please try a different search term or check for typos.</p>
            </div>
        );
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
