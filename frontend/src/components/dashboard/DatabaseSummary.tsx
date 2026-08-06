import React from 'react';
import WidgetCard from './WidgetCard';
import { DatabaseIcon } from '../icons';

interface DatabaseSummaryProps {
    version: string;
}

/**
 * Database summary panel. Record counts are honest placeholders —
 * the backend exposes no statistics endpoint yet.
 */
const DatabaseSummary: React.FC<DatabaseSummaryProps> = ({ version }) => {
    return (
        <WidgetCard title="Database Summary" icon={<DatabaseIcon />}>
            <div className="summary-row">
                <span className="summary-label">Source</span>
                <span className="summary-value">NVD dataset</span>
            </div>
            <div className="summary-row">
                <span className="summary-label">Records</span>
                <span className="summary-value placeholder">Pending stats</span>
            </div>
            <div className="summary-row">
                <span className="summary-label">Last updated</span>
                <span className="summary-value placeholder">Pending stats</span>
            </div>
            <div className="summary-row">
                <span className="summary-label">App version</span>
                <span className="summary-value mono">v{version}</span>
            </div>
        </WidgetCard>
    );
};

export default DatabaseSummary;
