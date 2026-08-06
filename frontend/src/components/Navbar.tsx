import React from 'react';
import { NavLink } from 'react-router-dom';
import '../styles/App.css';

const Navbar: React.FC = () => {
    return (
        <nav className="navbar">
            <div className="navbar-brand">
                <span className="brand-title">CyberRAG</span>
            </div>
            <ul className="navbar-links">
                <li>
                    <NavLink to="/search" className={({ isActive }) => (isActive ? 'active-link' : '')}>
                        Search
                    </NavLink>
                </li>
                <li>
                    <NavLink to="/ask" className={({ isActive }) => (isActive ? 'active-link' : '')}>
                        Ask
                    </NavLink>
                </li>
            </ul>
        </nav>
    );
};

export default Navbar;
