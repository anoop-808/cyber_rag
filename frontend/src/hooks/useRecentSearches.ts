import { useCallback } from 'react';
import { useLocalStorage } from './useLocalStorage';

const STORAGE_KEY = 'cyberrag.recentSearches';
const MAX_SEARCHES = 10;

/** Recent search queries persisted in localStorage (most recent first). */
export function useRecentSearches() {
    const [searches, setSearches] = useLocalStorage<string[]>(STORAGE_KEY, []);

    const addSearch = useCallback(
        (query: string) => {
            const trimmed = query.trim();
            if (!trimmed) return;
            setSearches((prev) => [trimmed, ...prev.filter((q) => q !== trimmed)].slice(0, MAX_SEARCHES));
        },
        [setSearches],
    );

    const clearSearches = useCallback(() => setSearches([]), [setSearches]);

    return { searches, addSearch, clearSearches };
}
