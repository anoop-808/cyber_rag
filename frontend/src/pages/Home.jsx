import React, { useState } from 'react';
import SearchBar from '../components/SearchBar';
import SearchResults from '../components/SearchResults';
import { searchCVEs } from '../services/api';

function Home() {
    const [results, setResults] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [hasSearched, setHasSearched] = useState(false);

    const handleSearch = async (query) => {
        setLoading(true);
        setError(null);
        setHasSearched(true);
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

    return (
        <div className="home">
            <header>
                <h1>CyberRAG</h1>
            </header>
            <main>
                <SearchBar onSearch={handleSearch} />
                <SearchResults
                    results={results}
                    loading={loading}
                    error={error}
                    hasSearched={hasSearched}
                />
            </main>
        </div>
    );
}
export default Home;
