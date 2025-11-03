import type { ReactNode } from "react";

export interface AlertProps {
    children: ReactNode;
    onDismiss: () => void;
}