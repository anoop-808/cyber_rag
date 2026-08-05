import React, { useState } from 'react';
import SearchBar from '../components/SearchBar';
import { searchCVEs } from '../services/api';

const SearchPage: React.FC = () => {
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const handleSearch = async (query: string, filters: Record<string, any>) => {
        if (!query.trim()) {
            setError('Query cannot be empty.');
            return;
        }

        setLoading(true);
        setError(null);

        try {
            // Deferring results implementation to TASK_024 per requirements.
            // Just making the API call to satisfy TASK_023 definition of done.
            await searchCVEs(query, filters);
        } catch (err: any) {
            if (err.response) {
                setError(`API Error: ${err.response.status} - Failed to fetch search results.`);
            } else if (err.request) {
                setError('Network Error: Unable to reach the backend.');
            } else {
                setError('An unexpected error occurred.');
            }
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="search-page">
            <header>
                <h1>Search Vulnerabilities</h1>
            </header>
            <main>
                <SearchBar onSearch={handleSearch} loading={loading} />

                {loading && (
                    <div className="loading-indicator">
                        <p>Loading results...</p>
                    </div>
                )}

                {error && (
                    <div className="error-message">
                        <p style={{ color: 'red' }}>{error}</p>
                    </div>
                )}
            </main>
        </div>
    );
};

export default SearchPage;
