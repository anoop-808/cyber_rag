import React, { ReactNode } from 'react';
import { Link } from 'react-router-dom';
import { ChevronRightIcon } from '../icons';

interface QuickActionCardProps {
    icon: ReactNode;
    title: string;
    description: string;
    /** Router path for navigable actions. */
    to?: string;
    /** Click handler for non-route actions. */
    onClick?: () => void;
    /** Disabled placeholder action (e.g. future integrations). */
    disabled?: boolean;
    /** Optional badge text (e.g. "Coming soon"). */
    badge?: string;
}

/**
 * Reusable quick-action card — icon, title, description, and a
 * navigational affordance. Disabled actions show a badge.
 */
const QuickActionCard: React.FC<QuickActionCardProps> = ({ icon, title, description, to, onClick, disabled, badge }) => {
    const content = (
        <>
            <span className="quick-action-icon">{icon}</span>
            <span className="quick-action-title-row">
                <span className="quick-action-title">{title}</span>
                {badge && <span className="quick-action-badge">{badge}</span>}
            </span>
            <p className="quick-action-desc">{description}</p>
            {!disabled && (
                <span className="quick-action-footer">
                    Open
                    <ChevronRightIcon />
                </span>
            )}
        </>
    );

    if (disabled) {
        return (
            <div className="quick-action disabled" aria-disabled="true">
                {content}
            </div>
        );
    }

    if (to) {
        return (
            <Link to={to} className="quick-action">
                {content}
            </Link>
        );
    }

    return (
        <button type="button" className="quick-action" onClick={onClick}>
            {content}
        </button>
    );
};

export default QuickActionCard;
