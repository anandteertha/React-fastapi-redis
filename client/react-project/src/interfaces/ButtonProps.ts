export interface ButtonProps {
    color?: 'primary' | 'secondary' | 'danger';
    children: string;
    onClick: () => void;
}