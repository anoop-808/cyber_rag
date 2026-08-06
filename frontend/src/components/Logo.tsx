import React from 'react';

interface LogoProps {
    size?: number;
}

/**
 * CyberRAG brand mark — a shield with a check, rendered in the
 * accent color. Styled via the .logo-icon class (currentColor).
 */
const Logo: React.FC<LogoProps> = ({ size = 18 }) => {
    return (
        <svg
            className="logo-icon"
            width={size}
            height={size}
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2.2"
            strokeLinecap="round"
            strokeLinejoin="round"
            aria-hidden="true"
        >
            <path d="M12 2l8 3.5v5.7c0 4.5-3.2 8.6-8 10.3-4.8-1.7-8-5.8-8-10.3V5.5L12 2z" />
            <path d="M8.5 12l2.5 2.5 4.5-4.5" />
        </svg>
    );
};

export default Logo;
