import React, { useState } from 'react';
import SearchBar from '../components/SearchBar';
import SearchResults from '../components/SearchResults';
import CVEDetail from '../components/CVEDetail';
import { searchCVEs } from '../services/api';

const Home: React.FC = () => {
    const [results, setResults] = useState<any[]>([]);
    const [loading, setLoading] = useState<boolean>(false);
    const [error, setError] = useState<string | null>(null);
    const [hasSearched, setHasSearched] = useState<boolean>(false);
    const [selectedCveId, setSelectedCveId] = useState<string | null>(null);
    const [searchQuery, setSearchQuery] = useState<string>('');

    const handleSearch = async (query: string) => {
        setSearchQuery(query);
        setLoading(true);
        setError(null);
        setHasSearched(true);
        setSelectedCveId(null);
        try {
            const data = await searchCVEs(query);
            setResults(data.results || []);
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
        <div className="home">
            <header>
                <h1>CyberRAG</h1>
            </header>
            <main>
                {selectedCveId ? (
                    <CVEDetail cveId={selectedCveId} onBack={handleBack} />
                ) : (
                    <>
                        <SearchBar onSearch={handleSearch} initialQuery={searchQuery} />
                        <SearchResults
                            results={results}
                            loading={loading}
                            error={error}
                            hasSearched={hasSearched}
                            onCveClick={handleCveClick}
                        />
                    </>
                )}
            </main>
        </div>
    );
};
export default Home;
