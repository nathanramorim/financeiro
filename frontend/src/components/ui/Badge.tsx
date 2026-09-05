import React from "react";

interface BadgeProps {
  variant?: "success" | "warning" | "danger" | "primary" | "neutral" | "accent";
  children: React.ReactNode;
  className?: string;
}

export const Badge: React.FC<BadgeProps> = ({
  variant = "neutral",
  children,
  className = "",
}) => {
  const variantStyles = {
    success: "bg-success-bg text-success border-success/30",
    warning: "bg-warning-bg text-warning border-warning/30",
    danger: "bg-danger-bg text-danger border-danger/30",
    primary: "bg-blue-50 text-primary border-primary/30",
    neutral: "bg-slate-100 text-slate-700 border-slate-200",
    accent: "bg-indigo-50 text-accent-indigo border-accent-indigo/30",
  };

  return (
    <span
      className={`inline-flex items-center px-2.5 py-0.5 rounded-pill text-xs font-semibold border ${variantStyles[variant]} ${className}`}
    >
      {children}
    </span>
  );
};
