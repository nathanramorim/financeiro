import React from "react";

interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  children: React.ReactNode;
  highlight?: boolean;
}

export const Card: React.FC<CardProps> = ({
  children,
  highlight = false,
  className = "",
  ...props
}) => {
  const borderStyle = highlight ? "border-primary/40 ring-1 ring-primary/20" : "border-panel-border";

  return (
    <div
      className={`bg-white rounded-card border ${borderStyle} shadow-sm p-4 sm:p-5 transition-all ${className}`}
      {...props}
    >
      {children}
    </div>
  );
};
