import React, { useCallback, useRef, useState } from 'react';
import { AnimatePresence, motion } from 'framer-motion';
import { fadeUpTransition } from '../motion';
import { CheckIcon, AlertIcon, InfoIcon } from '../icons';
import { ToastContext, type ToastKind } from './toast-context';

interface ToastItem {
    id: number;
    kind: ToastKind;
    message: string;
}

const TOAST_DURATION_MS = 3200;
const MAX_VISIBLE_TOASTS = 4;

const kindIcon: Record<ToastKind, React.ReactNode> = {
    success: <CheckIcon />,
    error: <AlertIcon size={16} />,
    info: <InfoIcon />,
};

export const ToastProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
    const [toasts, setToasts] = useState<ToastItem[]>([]);
    const idRef = useRef(0);

    const dismiss = useCallback((id: number) => {
        setToasts((current) => current.filter((toast) => toast.id !== id));
    }, []);

    const showToast = useCallback((message: string, kind: ToastKind = 'success') => {
        const id = ++idRef.current;
        setToasts((current) => [...current.slice(-(MAX_VISIBLE_TOASTS - 1)), { id, kind, message }]);
        window.setTimeout(() => dismiss(id), TOAST_DURATION_MS);
    }, [dismiss]);

    return (
        <ToastContext.Provider value={{ showToast }}>
            {children}
            <div className="toast-viewport" role="region" aria-live="polite" aria-label="Notifications">
                <AnimatePresence>
                    {toasts.map((toast) => (
                        <motion.div
                            key={toast.id}
                            className={`toast toast-${toast.kind}`}
                            initial={{ opacity: 0, y: 12, scale: 0.98 }}
                            animate={{ opacity: 1, y: 0, scale: 1 }}
                            exit={{ opacity: 0, y: 6, scale: 0.98 }}
                            transition={fadeUpTransition}
                            role="status"
                        >
                            <span className="toast-icon">{kindIcon[toast.kind]}</span>
                            {toast.message}
                        </motion.div>
                    ))}
                </AnimatePresence>
            </div>
        </ToastContext.Provider>
    );
};
