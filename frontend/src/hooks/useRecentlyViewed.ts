import { useCallback } from 'react';
import { useLocalStorage } from './useLocalStorage';

const STORAGE_KEY = 'cyberrag.recentlyViewed';
const MAX_VIEWED = 10;

/** Recently opened CVE IDs persisted in localStorage (most recent first). */
export function useRecentlyViewed() {
    const [viewed, setViewed] = useLocalStorage<string[]>(STORAGE_KEY, []);

    const addViewed = useCallback(
        (id: string) => {
            setViewed((prev) => [id, ...prev.filter((v) => v !== id)].slice(0, MAX_VIEWED));
        },
        [setViewed],
    );

    return { viewed, addViewed };
}
