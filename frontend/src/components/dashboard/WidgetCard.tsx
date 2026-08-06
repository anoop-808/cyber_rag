import React, { ReactNode } from 'react';

interface WidgetCardProps {
    title: string;
    icon: ReactNode;
    /** Optional header action (e.g. clear-history button). */
    action?: ReactNode;
    children: ReactNode;
    id?: string;
}

/** Shared widget shell used by all dashboard panels. */
const WidgetCard: React.FC<WidgetCardProps> = ({ title, icon, action, children, id }) => {
    return (
        <section className="widget-card" id={id} aria-label={title}>
            <div className="widget-header">
                <span className="widget-icon">{icon}</span>
                <h3 className="widget-title">{title}</h3>
                {action}
            </div>
            {children}
        </section>
    );
};

export default WidgetCard;
