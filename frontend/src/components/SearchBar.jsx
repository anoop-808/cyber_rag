import React, { useState } from 'react';

function SearchBar({ onSearch, initialQuery = '' }) {
    const [query, setQuery] = useState(initialQuery);

    const handleSubmit = (e) => {
        e.preventDefault();
        if (query.trim()) {
            onSearch(query);
        }
    };

    return (
        <form className="search-bar" onSubmit={handleSubmit}>
            <input
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Search vulnerabilities........"
            />
            <button type="submit">Search</button>
        </form>
    );
}
export default SearchBar;
