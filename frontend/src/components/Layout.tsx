import React, { ReactNode } from 'react';
import { useLocation } from 'react-router-dom';
import { motion } from 'framer-motion';
import Navbar from './Navbar';
import Logo from './Logo';
import { fadeUpTransition } from './motion';
import { version } from '../../package.json';
import '../styles/App.css';

interface LayoutProps {
    children: ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
    const location = useLocation();
    const year = new Date().getFullYear();

    return (
        <div className="layout-container">
            <header className="layout-header">
                <Navbar />
            </header>
            <main className="layout-main">
                {/* Keyed by pathname so each route change plays a subtle fade-up */}
                <motion.div
                    key={location.pathname}
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={fadeUpTransition}
                >
                    {children}
                </motion.div>
            </main>
            <footer className="layout-footer">
                <div className="footer-inner">
                    <div className="footer-brand">
                        <Logo size={16} />
                        <span>CyberRAG</span>
                    </div>
                    <div className="footer-links">
                        <a href="https://github.com/cyberrag/cyberrag" target="_blank" rel="noopener noreferrer">
                            GitHub
                        </a>
                    </div>
                    <div className="footer-meta">
                        <span>v{version}</span>
                        <span aria-hidden="true">·</span>
                        <span>&copy; {year} CyberRAG. All rights reserved.</span>
                    </div>
                </div>
            </footer>
        </div>
    );
};

export default Layout;
