import React, { useState } from 'react';
import SearchBar from '../components/SearchBar';
import SearchResults from '../components/SearchResults';
import CVEInfoCard from '../components/CVEInfoCard';
import Layout from '../components/Layout';
import { searchCVEs } from '../services/api';

function Home() {
    const [results, setResults] = useState<any[]>([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [hasSearched, setHasSearched] = useState(false);
    const [selectedCveId, setSelectedCveId] = useState<string | null>(null);
    const [searchQuery, setSearchQuery] = useState('');

    const handleSearch = async (query: string, filters: Record<string, any> = {}) => {
        setSearchQuery(query);
        setLoading(true);
        setError(null);
        setHasSearched(true);
        setSelectedCveId(null);
        try {
            const data = await searchCVEs(query, filters);
            // SearchResponse returns { documents: [...] }
            setResults(data.documents || data.results || []);
        } catch (err) {
            setError('Failed to fetch search results. Backend may be unavailable.');
            setResults([]);
        } finally {
            setLoading(false);
        }
    };

    const handleCveClick = (id: string) => {
        setSelectedCveId(id);
    };

    const handleBack = () => {
        setSelectedCveId(null);
    };

    return (
        <Layout>
            <div className="home-content">
                {selectedCveId ? (
                    <CVEInfoCard cveId={selectedCveId} onBack={handleBack} />
                ) : (
                    <>
                        <div className="page-header">
                            <h1>Search Vulnerabilities</h1>
                            <p className="page-description">Find the latest Common Vulnerabilities and Exposures (CVEs).</p>
                        </div>
                        <SearchBar onSearch={handleSearch} initialQuery={searchQuery} loading={loading} />
                        <SearchResults
                            results={results}
                            loading={loading}
                            error={error}
                            hasSearched={hasSearched}
                            onCveClick={handleCveClick}
                        />
                    </>
                )}
            </div>
        </Layout>
    );
}
export default Home;
