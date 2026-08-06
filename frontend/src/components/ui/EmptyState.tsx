import React, { ReactNode } from 'react';
import { SearchIcon } from '../icons';

interface EmptyStateProps {
    title?: string;
    message?: string;
    /** Custom icon node; defaults to a search icon. */
    icon?: ReactNode;
    /** Optional action element rendered below the message. */
    action?: ReactNode;
}

/**
 * Reusable empty state — friendly guidance with an icon when a
 * page or list has no data yet.
 */
const EmptyState: React.FC<EmptyStateProps> = ({
    title = 'Nothing here yet',
    message,
    icon,
    action,
}) => {
    return (
        <div className="empty-state">
            <div className="state-icon" aria-hidden="true">
                {icon ?? <SearchIcon />}
            </div>
            <h3 className="state-title">{title}</h3>
            {message && <p className="state-message">{message}</p>}
            {action && <div className="state-action">{action}</div>}
        </div>
    );
};

export default EmptyState;
