import React, { useEffect, useState } from 'react';
import { NavLink, useLocation } from 'react-router-dom';
import Logo from './Logo';
import '../styles/App.css';

const MenuIcon: React.FC = () => (
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" aria-hidden="true">
        <path d="M4 6h16" />
        <path d="M4 12h16" />
        <path d="M4 18h16" />
    </svg>
);

const CloseIcon: React.FC = () => (
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" aria-hidden="true">
        <path d="M6 6l12 12" />
        <path d="M18 6L6 18" />
    </svg>
);

const Navbar: React.FC = () => {
    const [menuOpen, setMenuOpen] = useState(false);
    const location = useLocation();

    // Close the mobile menu with Escape and after navigating
    // (link clicks, browser back/forward, or programmatic nav).
    useEffect(() => {
        if (!menuOpen) return;
        const onKey = (e: KeyboardEvent) => {
            if (e.key === 'Escape') setMenuOpen(false);
        };
        window.addEventListener('keydown', onKey);
        return () => window.removeEventListener('keydown', onKey);
    }, [menuOpen]);

    useEffect(() => {
        setMenuOpen(false);
    }, [location.pathname]);

    const closeMenu = () => setMenuOpen(false);

    return (
        <nav className="navbar" aria-label="Primary">
            <div className="navbar-brand">
                <NavLink to="/" className="brand-link" onClick={closeMenu}>
                    <span className="brand-logo">
                        <Logo />
                    </span>
                    <span className="brand-title">CyberRAG</span>
                </NavLink>
            </div>

            <button
                type="button"
                className="nav-toggle"
                aria-expanded={menuOpen}
                aria-controls="main-nav-links"
                aria-label={menuOpen ? 'Close navigation menu' : 'Open navigation menu'}
                onClick={() => setMenuOpen((open) => !open)}
            >
                {menuOpen ? <CloseIcon /> : <MenuIcon />}
            </button>

            <ul id="main-nav-links" className={`navbar-links${menuOpen ? ' open' : ''}`}>
                <li>
                    <NavLink
                        to="/search"
                        className={({ isActive }) => (isActive ? 'active-link' : '')}
                        onClick={closeMenu}
                    >
                        Search
                    </NavLink>
                </li>
                <li>
                    <NavLink
                        to="/ask"
                        className={({ isActive }) => (isActive ? 'active-link' : '')}
                        onClick={closeMenu}
                    >
                        Ask AI
                    </NavLink>
                </li>
            </ul>
        </nav>
    );
};

export default Navbar;
