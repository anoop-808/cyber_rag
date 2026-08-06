import React, { ReactNode } from 'react';
import Navbar from './Navbar';
import '../styles/App.css';

interface LayoutProps {
    children: ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
    return (
        <div className="layout-container">
            <header className="layout-header">
                <Navbar />
            </header>
            <main className="layout-main">
                {children}
            </main>
            <footer className="layout-footer">
                <p>&copy; {new Date().getFullYear()} CyberRAG. All rights reserved.</p>
            </footer>
        </div>
    );
};

export default Layout;
