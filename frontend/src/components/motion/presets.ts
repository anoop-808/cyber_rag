import type { Easing, Transition } from 'framer-motion';

/**
 * Shared motion configuration for the CyberRAG design system.
 * Single source of truth for animation timing & easing so
 * every animated surface moves with the same character.
 */

/** Signature ease — smooth deceleration, no bounce. */
export const easeOut: Easing = [0.16, 1, 0.3, 1];

/** Fade + slide-up for page & section entrances. */
export const fadeUpTransition: Transition = {
    duration: 0.35,
    ease: easeOut,
};
