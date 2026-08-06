import React, { useState } from 'react';
import SearchBar from '../components/SearchBar';
import SearchResults from '../components/SearchResults';
import CVEInfoCard from '../components/CVEInfoCard';
import Layout from '../components/Layout';
import { PageHeader } from '../components/ui';
import { useToast } from '../components/ui/toast-context';
import {
    StatCard,
    QuickActionCard,
    WidgetCard,
    RecentSearches,
    FavoritesList,
    RecentlyViewedList,
    DatabaseSummary,
} from '../components/dashboard';
import { SearchIcon, ChatIcon, ListIcon, PlugIcon, DatabaseIcon, ActivityIcon, AlertIcon } from '../components/icons';
import { useRecentSearches } from '../hooks/useRecentSearches';
import { useRecentlyViewed } from '../hooks/useRecentlyViewed';
import { useFavorites } from '../hooks/useFavorites';
import { searchCVEs } from '../services/api';
import { version } from '../../package.json';

const STATS = [
    { label: 'Total CVEs', tone: 'default' as const, icon: <DatabaseIcon size={20} /> },
    { label: 'Critical', tone: 'critical' as const, icon: <AlertIcon size={20} /> },
    { label: 'High', tone: 'high' as const, icon: <AlertIcon size={20} /> },
    { label: 'Medium', tone: 'medium' as const, icon: <AlertIcon size={20} /> },
    { label: 'Low', tone: 'low' as const, icon: <AlertIcon size={20} /> },
];

function Home() {
    const { showToast } = useToast();
    const { searches, addSearch, clearSearches } = useRecentSearches();
    const { viewed } = useRecentlyViewed();
    const { favorites, removeFavorite } = useFavorites();

    const [results, setResults] = useState<any[]>([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [hasSearched, setHasSearched] = useState(false);
    const [selectedCveId, setSelectedCveId] = useState<string | null>(null);
    const [searchQuery, setSearchQuery] = useState('');

    const handleSearch = async (query: string, filters: Record<string, any> = {}) => {
        setSearchQuery(query);
        addSearch(query);
        setLoading(true);
        setError(null);
        setHasSearched(true);
        setSelectedCveId(null);
        try {
            const data = await searchCVEs(query, filters);
            // SearchResponse returns { documents: [...] }
            const docs = data.documents || data.results || [];
            setResults(docs);
            if (docs.length > 0) {
                showToast('Search completed');
            }
        } catch {
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

    const scrollToActivity = () => {
        const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
        document
            .getElementById('dashboard-activity')
            ?.scrollIntoView({ behavior: reduceMotion ? 'auto' : 'smooth', block: 'start' });
    };

    return (
        <Layout>
            <div className="home-content dashboard">
                {selectedCveId ? (
                    <CVEInfoCard cveId={selectedCveId} onBack={handleBack} />
                ) : (
                    <>
                        <PageHeader
                            title="Security Dashboard"
                            subtitle="Monitor the vulnerability database and investigate threats with CyberRAG."
                        />

                        <section className="stats-grid" aria-label="Database statistics">
                            {STATS.map((stat) => (
                                <StatCard key={stat.label} {...stat} value={null} placeholder />
                            ))}
                        </section>
                        <p className="stats-disclaimer">
                            Statistics are placeholders until a backend stats endpoint is available.
                        </p>

                        <section className="quick-actions" aria-label="Quick actions">
                            <QuickActionCard
                                icon={<SearchIcon />}
                                title="Search Vulnerabilities"
                                description="Keyword and semantic search across the CVE database."
                                to="/search"
                            />
                            <QuickActionCard
                                icon={<ChatIcon />}
                                title="Ask AI"
                                description="Get grounded answers to your security questions."
                                to="/ask"
                            />
                            <QuickActionCard
                                icon={<ListIcon />}
                                title="Browse Recent CVEs"
                                description="Jump to your recently viewed and favorited records."
                                onClick={scrollToActivity}
                            />
                            <QuickActionCard
                                icon={<PlugIcon />}
                                title="Future Integrations"
                                description="Vendor feeds, KEV, and exploit intelligence."
                                disabled
                                badge="Coming soon"
                            />
                        </section>

                        <section className="dashboard-search" aria-label="Search">
                            <SearchBar onSearch={handleSearch} initialQuery={searchQuery} loading={loading} />
                        </section>

                        <SearchResults
                            results={results}
                            loading={loading}
                            error={error}
                            hasSearched={hasSearched}
                            onCveClick={handleCveClick}
                            onRetry={() => handleSearch(searchQuery)}
                        />

                        <div className="dashboard-widgets" id="dashboard-activity">
                            <RecentSearches searches={searches} onSelect={handleSearch} onClear={clearSearches} />
                            <RecentlyViewedList viewed={viewed} />
                            <FavoritesList favorites={favorites} onRemove={removeFavorite} />
                        </div>

                        <div className="dashboard-grid">
                            <DatabaseSummary version={version} />
                            <WidgetCard title="Recent Activity" icon={<ActivityIcon />}>
                                <p className="widget-empty">
                                    Activity telemetry is not enabled yet. Ingestion and search activity will appear here in a
                                    future release.
                                </p>
                            </WidgetCard>
                        </div>
                    </>
                )}
            </div>
        </Layout>
    );
}
export default Home;
