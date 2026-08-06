import React from 'react';
import { motion, type HTMLMotionProps } from 'framer-motion';
import { fadeUpTransition } from './presets';

interface FadeInProps extends HTMLMotionProps<'div'> {
    /** Stagger delay in seconds. */
    delay?: number;
    /** Initial vertical offset in px. */
    y?: number;
}

/**
 * Reusable entrance animation — fades content in with a subtle
 * slide-up. Respects the global reduced-motion preference via
 * Framer Motion's useReducedMotion-aware defaults.
 */
const FadeIn: React.FC<FadeInProps> = ({ children, delay = 0, y = 10, ...rest }) => {
    return (
        <motion.div
            initial={{ opacity: 0, y }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ ...fadeUpTransition, delay }}
            {...rest}
        >
            {children}
        </motion.div>
    );
};

export default FadeIn;
