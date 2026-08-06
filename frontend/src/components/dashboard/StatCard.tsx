import React, { ReactNode } from 'react';

interface StatCardProps {
    label: string;
    /** Raw value; null/undefined renders a placeholder dash. */
    value: number | string | null;
    icon: ReactNode;
    tone?: 'default' | 'critical' | 'high' | 'medium' | 'low';
    /** Mark the value as a placeholder when backend stats are unavailable. */
    placeholder?: boolean;
}

/**
 * Reusable statistic card — icon, headline value, and label.
 * Never invents data: placeholder values are clearly marked.
 */
const StatCard: React.FC<StatCardProps> = ({ label, value, icon, tone = 'default', placeholder = false }) => {
    return (
        <div className={`stat-card stat-${tone}`}>
            <div className="stat-icon">{icon}</div>
            <div className="stat-body">
                <span className="stat-value">{placeholder ? '—' : (value ?? '—')}</span>
                <span className="stat-label">{label}</span>
                {placeholder && <span className="stat-note">Placeholder</span>}
            </div>
        </div>
    );
};

export default StatCard;
