import { useCallback } from 'react';
import { useLocalStorage } from './useLocalStorage';

const STORAGE_KEY = 'cyberrag.favorites';

/** Bookmarked CVE IDs persisted in localStorage. */
export function useFavorites() {
    const [favorites, setFavorites] = useLocalStorage<string[]>(STORAGE_KEY, []);

    const toggleFavorite = useCallback(
        (id: string) => {
            setFavorites((prev) => (prev.includes(id) ? prev.filter((f) => f !== id) : [id, ...prev]));
        },
        [setFavorites],
    );

    const removeFavorite = useCallback(
        (id: string) => {
            setFavorites((prev) => prev.filter((f) => f !== id));
        },
        [setFavorites],
    );

    return { favorites, toggleFavorite, removeFavorite };
}
