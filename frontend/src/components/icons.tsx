import React from 'react';

interface IconProps {
    size?: number;
}

/**
 * Shared inline icon set — single source of truth for the small
 * UI glyphs used across the application. All icons inherit
 * currentColor and are hidden from assistive technology.
 */
const base = { fill: 'none', stroke: 'currentColor', strokeWidth: 2, strokeLinecap: 'round', strokeLinejoin: 'round' } as const;

export const SearchIcon: React.FC<IconProps> = ({ size = 18 }) => (
    <svg width={size} height={size} viewBox="0 0 24 24" {...base} aria-hidden="true">
        <circle cx="11" cy="11" r="7" />
        <path d="M21 21l-4.3-4.3" />
    </svg>
);

export const CopyIcon: React.FC<IconProps> = ({ size = 15 }) => (
    <svg width={size} height={size} viewBox="0 0 24 24" {...base} aria-hidden="true">
        <rect x="9" y="9" width="12" height="12" rx="2" />
        <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1" />
    </svg>
);

export const CheckIcon: React.FC<IconProps> = ({ size = 15 }) => (
    <svg width={size} height={size} viewBox="0 0 24 24" {...base} strokeWidth={2.4} aria-hidden="true">
        <path d="M20 6L9 17l-5-5" />
    </svg>
);

export const AlertIcon: React.FC<IconProps> = ({ size = 26 }) => (
    <svg width={size} height={size} viewBox="0 0 24 24" {...base} strokeWidth={1.8} aria-hidden="true">
        <path d="M12 3l10 17H2L12 3z" />
        <path d="M12 10v4" />
        <path d="M12 17.5h.01" />
    </svg>
);

export const ExternalLinkIcon: React.FC<IconProps> = ({ size = 13 }) => (
    <svg width={size} height={size} viewBox="0 0 24 24" {...base} aria-hidden="true">
        <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6" />
        <path d="M15 3h6v6" />
        <path d="M10 14L21 3" />
    </svg>
);

export const ChatIcon: React.FC<IconProps> = ({ size = 15 }) => (
    <svg width={size} height={size} viewBox="0 0 24 24" {...base} aria-hidden="true">
        <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" />
        <path d="M9 9h6" />
        <path d="M9 12h4" />
    </svg>
);

export const InfoIcon: React.FC<IconProps> = ({ size = 16 }) => (
    <svg width={size} height={size} viewBox="0 0 24 24" {...base} aria-hidden="true">
        <circle cx="12" cy="12" r="9" />
        <path d="M12 8h.01" />
        <path d="M12 12v4" />
    </svg>
);

export const QuestionIcon: React.FC<IconProps> = ({ size = 26 }) => (
    <svg width={size} height={size} viewBox="0 0 24 24" {...base} strokeWidth={1.8} aria-hidden="true">
        <circle cx="12" cy="12" r="9" />
        <path d="M9.5 9.5a2.5 2.5 0 1 1 3.7 2.2c-.8.4-1.2 1-1.2 1.8" />
        <path d="M12 17.5h.01" />
    </svg>
);

export const StarIcon: React.FC<IconProps & { filled?: boolean }> = ({ size = 16, filled = false }) => (
    <svg
        width={size}
        height={size}
        viewBox="0 0 24 24"
        fill={filled ? 'currentColor' : 'none'}
        stroke="currentColor"
        strokeWidth="2"
        strokeLinecap="round"
        strokeLinejoin="round"
        aria-hidden="true"
    >
        <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z" />
    </svg>
);

export const ClockIcon: React.FC<IconProps> = ({ size = 16 }) => (
    <svg width={size} height={size} viewBox="0 0 24 24" {...base} aria-hidden="true">
        <circle cx="12" cy="12" r="9" />
        <path d="M12 7v5l3 3" />
    </svg>
);

export const DatabaseIcon: React.FC<IconProps> = ({ size = 16 }) => (
    <svg width={size} height={size} viewBox="0 0 24 24" {...base} aria-hidden="true">
        <ellipse cx="12" cy="5" rx="8" ry="3" />
        <path d="M4 5v14c0 1.7 3.6 3 8 3s8-1.3 8-3V5" />
        <path d="M4 12c0 1.7 3.6 3 8 3s8-1.3 8-3" />
    </svg>
);

export const ListIcon: React.FC<IconProps> = ({ size = 16 }) => (
    <svg width={size} height={size} viewBox="0 0 24 24" {...base} aria-hidden="true">
        <path d="M8 6h13" />
        <path d="M8 12h13" />
        <path d="M8 18h13" />
        <path d="M3 6h.01" />
        <path d="M3 12h.01" />
        <path d="M3 18h.01" />
    </svg>
);

export const PlugIcon: React.FC<IconProps> = ({ size = 16 }) => (
    <svg width={size} height={size} viewBox="0 0 24 24" {...base} aria-hidden="true">
        <path d="M9 2v6" />
        <path d="M15 2v6" />
        <path d="M6 8h12v3a6 6 0 0 1-12 0V8z" />
        <path d="M12 17v5" />
    </svg>
);

export const ActivityIcon: React.FC<IconProps> = ({ size = 16 }) => (
    <svg width={size} height={size} viewBox="0 0 24 24" {...base} aria-hidden="true">
        <path d="M22 12h-4l-3 8-6-16-3 8H2" />
    </svg>
);

export const ChevronRightIcon: React.FC<IconProps> = ({ size = 14 }) => (
    <svg width={size} height={size} viewBox="0 0 24 24" {...base} aria-hidden="true">
        <path d="M9 6l6 6-6 6" />
    </svg>
);
