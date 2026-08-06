import React from 'react';
import { Link } from 'react-router-dom';
import WidgetCard from './WidgetCard';
import { ActivityIcon } from '../icons';

interface RecentlyViewedListProps {
    viewed: string[];
}

/** Recently opened CVE IDs widget. */
const RecentlyViewedList: React.FC<RecentlyViewedListProps> = ({ viewed }) => {
    return (
        <WidgetCard title="Recently Viewed" icon={<ActivityIcon />}>
            {viewed.length === 0 ? (
                <p className="widget-empty">No CVEs viewed yet. Open a record to track it here.</p>
            ) : (
                <ul className="widget-list">
                    {viewed.map((id) => (
                        <li className="widget-item" key={id}>
                            <Link to={`/cve/${id}`} className="widget-item-link mono">
                                {id}
                            </Link>
                        </li>
                    ))}
                </ul>
            )}
        </WidgetCard>
    );
};

export default RecentlyViewedList;
