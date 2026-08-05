import React from 'react';
import '../styles/App.css'; // Make sure styles are applied (or we can add specific styles to App.css)

interface SeverityBadgeProps {
    severity: string | undefined | null;
}

const SeverityBadge: React.FC<SeverityBadgeProps> = ({ severity }) => {
    const normalizedSeverity = (severity || 'UNKNOWN').toUpperCase();

    // Mapping for classes (handled in App.css)
    let badgeClass = 'severity-badge ';
    switch (normalizedSeverity) {
        case 'CRITICAL':
            badgeClass += 'critical';
            break;
        case 'HIGH':
            badgeClass += 'high';
            break;
        case 'MEDIUM':
            badgeClass += 'medium';
            break;
        case 'LOW':
            badgeClass += 'low';
            break;
        default:
            badgeClass += 'unknown';
            break;
    }

    return (
        <span className={badgeClass}>
            {normalizedSeverity}
        </span>
    );
};

export default SeverityBadge;
