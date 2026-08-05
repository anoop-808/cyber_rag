import React from 'react';
import SearchResultCard from './SearchResultCard';

interface SearchResultsProps {
    results: any[];
    loading: boolean;
    error: string | null;
    hasSearched: boolean;
    onCveClick?: (id: string) => void;
}

function SearchResults({ results, loading, error, hasSearched, onCveClick }: SearchResultsProps) {
    if (loading) {
        return (
            <div className="loading">
                <p>Loading placeholders...</p>
                {/* Skeletons could go here */}
            </div>
        );
    }

    if (error) {
        return (
            <div className="error">
                <p>{error}</p>
            </div>
        );
    }

    if (hasSearched && results.length === 0) {
        return (
            <div className="no-results">
                <p>No vulnerabilities found.</p>
                <p>Try another search.</p>
            </div>
        );
    }

    if (!hasSearched) {
        return null; // Return null if nothing has happened yet
    }

    return (
        <div className="search-results-container">
            <div className="result-count" style={{ marginBottom: '1rem', fontWeight: 'bold' }}>
                <p>{results.length} Results Found</p>
            </div>
            <div className="search-results">
                {results.map((cve) => (
                    <SearchResultCard key={cve.id} cve={cve} onClick={onCveClick} />
                ))}
            </div>
        </div>
    );
}

export default SearchResults;
