import React from "react";
export interface ButtonProps {
    onClick: () => void;
    align: string
    children?: React.ReactNode
}