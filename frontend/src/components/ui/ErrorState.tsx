import React from 'react';
import { AlertIcon } from '../icons';

interface ErrorStateProps {
    /** Helpful, human-readable error message. */
    message: string;
    title?: string;
    /** Optional retry handler; renders a "Try again" button when provided. */
    onRetry?: () => void;
}

/**
 * Reusable error state — accessible alert with an icon, message,
 * and optional retry action.
 */
const ErrorState: React.FC<ErrorStateProps> = ({ message, title = 'Something went wrong', onRetry }) => {
    return (
        <div className="error-state" role="alert">
            <div className="state-icon" aria-hidden="true">
                <AlertIcon />
            </div>
            <h3 className="state-title">{title}</h3>
            <p className="state-message">{message}</p>
            {onRetry && (
                <div className="state-action">
                    <button type="button" className="btn btn-secondary" onClick={onRetry}>
                        Try again
                    </button>
                </div>
            )}
        </div>
    );
};

export default ErrorState;
