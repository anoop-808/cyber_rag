import { useCallback, useState } from 'react';

/**
 * Generic localStorage-backed state hook. Falls back to in-memory
 * state when storage is unavailable (private mode, quota, SSR).
 */
export function useLocalStorage<T>(key: string, initialValue: T) {
    const [value, setValue] = useState<T>(() => {
        try {
            const raw = window.localStorage.getItem(key);
            return raw !== null ? (JSON.parse(raw) as T) : initialValue;
        } catch {
            return initialValue;
        }
    });

    const set = useCallback(
        (next: T | ((prev: T) => T)) => {
            setValue((prev) => {
                const resolved = typeof next === 'function' ? (next as (p: T) => T)(prev) : next;
                try {
                    window.localStorage.setItem(key, JSON.stringify(resolved));
                } catch {
                    // Keep in-memory state when persistence is unavailable.
                }
                return resolved;
            });
        },
        [key],
    );

    return [value, set] as const;
}
