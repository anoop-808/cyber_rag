import React from 'react';
import { Link } from 'react-router-dom';
import WidgetCard from './WidgetCard';
import { StarIcon } from '../icons';

interface FavoritesListProps {
    favorites: string[];
    onRemove: (id: string) => void;
}

/** Bookmarked CVE IDs widget with per-item removal. */
const FavoritesList: React.FC<FavoritesListProps> = ({ favorites, onRemove }) => {
    return (
        <WidgetCard title="Favorites" icon={<StarIcon filled />}>
            {favorites.length === 0 ? (
                <p className="widget-empty">No favorites yet. Star a CVE to pin it here.</p>
            ) : (
                <ul className="widget-list">
                    {favorites.map((id) => (
                        <li className="widget-item" key={id}>
                            <Link to={`/cve/${id}`} className="widget-item-link mono">
                                {id}
                            </Link>
                            <button
                                type="button"
                                className="widget-item-remove"
                                onClick={() => onRemove(id)}
                                aria-label={`Remove ${id} from favorites`}
                            >
                                ×
                            </button>
                        </li>
                    ))}
                </ul>
            )}
        </WidgetCard>
    );
};

export default FavoritesList;
