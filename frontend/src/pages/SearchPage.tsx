import React, { useState } from 'react';
import SearchBar from '../components/SearchBar';
import SearchResults from '../components/SearchResults';
import Layout from '../components/Layout';
import { searchCVEs } from '../services/api';

const SearchPage: React.FC = () => {
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [results, setResults] = useState<any[]>([]);
    const [hasSearched, setHasSearched] = useState(false);

    const handleSearch = async (query: string, filters: Record<string, any>) => {
        if (!query.trim()) {
            setError('Query cannot be empty.');
            return;
        }

        setLoading(true);
        setError(null);
        setHasSearched(true);
        setResults([]);

        try {
            const data = await searchCVEs(query, filters);
            // API returns SearchResponse with { documents: [...] }
            setResults(data.documents || data.results || []);
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
        <Layout>
            <div className="search-page-content">
                <div className="page-header">
                    <h1>Search Vulnerabilities</h1>
                    <p className="page-description">Find the latest Common Vulnerabilities and Exposures (CVEs).</p>
                </div>

                <SearchBar onSearch={handleSearch} loading={loading} />

                <SearchResults
                    results={results}
                    loading={loading}
                    error={error}
                    hasSearched={hasSearched}
                />
            </div>
        </Layout>
    );
};

export default SearchPage;
