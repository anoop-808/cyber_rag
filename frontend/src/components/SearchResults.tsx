import React from 'react';
import SearchResultCard from './SearchResultCard';
import { FadeIn } from './motion';
import { LoadingState, EmptyState, ErrorState } from './ui';

interface SearchResultsProps {
    results: any[];
    loading: boolean;
    error: string | null;
    hasSearched: boolean;
    onCveClick?: (id: string) => void;
    onRetry?: () => void;
}

function SearchResults({ results, loading, error, hasSearched, onCveClick, onRetry }: SearchResultsProps) {
    if (loading) {
        return <LoadingState label="Searching..." skeleton />;
    }

    if (error) {
        return <ErrorState message={error} onRetry={onRetry} />;
    }

    if (hasSearched && results.length === 0) {
        return (
            <EmptyState
                title="No vulnerabilities found"
                message="Try different keywords, check the spelling, or remove severity filters to broaden your search."
            />
        );
    }

    if (!hasSearched) {
        return null; // Return null if nothing has happened yet
    }

    return (
        <FadeIn>
            <div className="search-results-container">
                <div className="result-count">
                    <p><strong>{results.length}</strong> Results Found</p>
                </div>
                <div className="search-results">
                    {results.map((cve) => (
                        <SearchResultCard key={cve.id} cve={cve} onClick={onCveClick} />
                    ))}
                </div>
            </div>
        </FadeIn>
    );
}

export default SearchResults;
