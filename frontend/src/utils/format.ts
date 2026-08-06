/**
 * Shared display-formatting helpers for the CyberRAG frontend.
 */

/**
 * Format a date value into a compact, human-readable string.
 * Returns null when the value is missing or unparseable so
 * callers can hide the field gracefully.
 */
export function formatDate(value: string | number | null | undefined): string | null {
    if (value === null || value === undefined || value === '') return null;
    const date = new Date(value);
    if (Number.isNaN(date.getTime())) return null;
    return date.toLocaleDateString(undefined, {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
    });
}

/**
 * Normalize a severity value to its lowercase level used for
 * color modifiers (critical/high/medium/low/unknown).
 */
export function severityLevel(severity?: string | null): string {
    return (severity || 'UNKNOWN').toLowerCase();
}

/**
 * Convert a CVSS score (0-10) to a 0-100 percentage for the
 * meter visualization. Returns null when the score is missing
 * or unparseable so callers can hide the meter gracefully.
 */
export function cvssPercent(score: unknown): number | null {
    if (score === null || score === undefined || Number.isNaN(Number(score))) return null;
    return Math.min(100, Math.max(0, Number(score) * 10));
}

/**
 * Copy text to the clipboard with a fallback for non-secure
 * contexts (execCommand). Returns true on success.
 */
export async function copyToClipboard(text: string): Promise<boolean> {
    try {
        if (navigator.clipboard && typeof navigator.clipboard.writeText === 'function') {
            await navigator.clipboard.writeText(text);
            return true;
        }
    } catch {
        // Fall through to the legacy path below.
    }

    try {
        const textarea = document.createElement('textarea');
        textarea.value = text;
        textarea.style.position = 'fixed';
        textarea.style.opacity = '0';
        document.body.appendChild(textarea);
        textarea.select();
        const ok = document.execCommand('copy');
        document.body.removeChild(textarea);
        return ok;
    } catch {
        return false;
    }
}
