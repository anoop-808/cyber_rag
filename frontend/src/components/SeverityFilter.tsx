import React from 'react';

interface SeverityFilterProps {
    value: string;
    onChange: (value: string) => void;
    disabled?: boolean;
}

const SeverityFilter: React.FC<SeverityFilterProps> = ({ value, onChange, disabled }) => {
    return (
        <div className="severity-filter">
            <label htmlFor="severity-select">Severity: </label>
            <select
                id="severity-select"
                value={value}
                onChange={(e) => onChange(e.target.value)}
                disabled={disabled}
            >
                <option value="">All Severities</option>
                <option value="CRITICAL">CRITICAL</option>
                <option value="HIGH">HIGH</option>
                <option value="MEDIUM">MEDIUM</option>
                <option value="LOW">LOW</option>
            </select>
        </div>
    );
};

export default SeverityFilter;
