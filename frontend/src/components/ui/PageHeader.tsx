import React, { ReactNode } from 'react';

interface PageHeaderProps {
    title: string;
    subtitle?: string;
    /** Optional action elements (e.g. buttons) rendered under the subtitle. */
    actions?: ReactNode;
}

/**
 * Reusable page header — consistent title/subtitle/actions block
 * for every page in the application.
 */
const PageHeader: React.FC<PageHeaderProps> = ({ title, subtitle, actions }) => {
    return (
        <header className="page-header">
            <h1>{title}</h1>
            {subtitle && <p className="page-description">{subtitle}</p>}
            {actions && <div className="page-header-actions">{actions}</div>}
        </header>
    );
};

export default PageHeader;
