import React from 'react';

interface LoadingStateProps {
    /** Screen-reader label announcing the loading state. */
    label?: string;
    /** Render skeleton placeholder cards instead of a text label. */
    skeleton?: boolean;
}

/**
 * Reusable loading state — accessible status region with either a
 * subtle pulsing label or shimmer skeleton cards (no spinners).
 */
const LoadingState: React.FC<LoadingStateProps> = ({ label = 'Loading...', skeleton = false }) => {
    if (skeleton) {
        return (
            <div className="loading-state skeleton-state" role="status" aria-live="polite" aria-label={label}>
                <div className="skeleton-card" aria-hidden="true">
                    <span className="skeleton-line skeleton-title" />
                    <span className="skeleton-line" />
                    <span className="skeleton-line" />
                    <span className="skeleton-line skeleton-short" />
                </div>
                <div className="skeleton-card" aria-hidden="true">
                    <span className="skeleton-line skeleton-title" />
                    <span className="skeleton-line" />
                    <span className="skeleton-line skeleton-short" />
                </div>
            </div>
        );
    }

    return (
        <div className="loading-state" role="status" aria-live="polite">
            <p>{label}</p>
        </div>
    );
};

export default LoadingState;
