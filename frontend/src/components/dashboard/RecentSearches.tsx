import React from 'react';
import WidgetCard from './WidgetCard';
import { ClockIcon } from '../icons';

interface RecentSearchesProps {
    searches: string[];
    onSelect: (query: string) => void;
    onClear: () => void;
}

/** Recent search queries widget — clicking an item reruns the search. */
const RecentSearches: React.FC<RecentSearchesProps> = ({ searches, onSelect, onClear }) => {
    return (
        <WidgetCard
            title="Recent Searches"
            icon={<ClockIcon />}
            action={
                <button type="button" className="widget-clear" onClick={onClear} disabled={searches.length === 0}>
                    Clear
                </button>
            }
        >
            {searches.length === 0 ? (
                <p className="widget-empty">No recent searches yet. Run a search to see it here.</p>
            ) : (
                <ul className="widget-list">
                    {searches.map((query) => (
                        <li className="widget-item" key={query}>
                            <button
                                type="button"
                                className="widget-item-link"
                                onClick={() => onSelect(query)}
                                title={`Search again: ${query}`}
                            >
                                {query}
                            </button>
                        </li>
                    ))}
                </ul>
            )}
        </WidgetCard>
    );
};

export default RecentSearches;
