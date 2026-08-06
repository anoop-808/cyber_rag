import React, { useState } from 'react';
import SearchBar from '../components/SearchBar';
import SearchResults from '../components/SearchResults';
import Layout from '../components/Layout';
import { PageHeader } from '../components/ui';
import { useToast } from '../components/ui/toast-context';
import { useRecentSearches } from '../hooks/useRecentSearches';
import { searchCVEs } from '../services/api';

const SearchPage: React.FC = () => {
    const { showToast } = useToast();
    const { addSearch } = useRecentSearches();
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [results, setResults] = useState<any[]>([]);
    const [hasSearched, setHasSearched] = useState(false);
    const [lastQuery, setLastQuery] = useState('');
    const [lastFilters, setLastFilters] = useState<Record<string, any>>({});

    const handleSearch = async (query: string, filters: Record<string, any>) => {
        if (!query.trim()) {
            setError('Query cannot be empty.');
            return;
        }

        setLastQuery(query);
        setLastFilters(filters);
        addSearch(query);
        setLoading(true);
        setError(null);
        setHasSearched(true);
        setResults([]);

        try {
            const data = await searchCVEs(query, filters);
            // API returns SearchResponse with { documents: [...] }
            const docs = data.documents || data.results || [];
            setResults(docs);
            if (docs.length > 0) {
                showToast('Search completed');
            }
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
                <PageHeader
                    title="Search Vulnerabilities"
                    subtitle="Find the latest Common Vulnerabilities and Exposures (CVEs)."
                />

                <SearchBar onSearch={handleSearch} loading={loading} />

                <SearchResults
                    results={results}
                    loading={loading}
                    error={error}
                    hasSearched={hasSearched}
                    onRetry={() => lastQuery && handleSearch(lastQuery, lastFilters)}
                />
            </div>
        </Layout>
    );
};

export default SearchPage;
