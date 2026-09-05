import React from "react";
import ReactMarkdown from "react-markdown";

interface MarkdownRendererProps {
  content: string;
  className?: string;
}

export const MarkdownRenderer: React.FC<MarkdownRendererProps> = ({
  content,
  className = "",
}) => {
  return (
    <div className={`prose-sm text-sm leading-relaxed ${className}`}>
      <ReactMarkdown
        components={{
          h1: ({ children }) => (
            <h1 className="text-lg font-bold text-text mt-2 mb-1.5">
              {children}
            </h1>
          ),
          h2: ({ children }) => (
            <h2 className="text-base font-bold text-text mt-2.5 mb-1.5">
              {children}
            </h2>
          ),
          h3: ({ children }) => (
            <h3 className="text-sm sm:text-base font-bold text-text mt-2.5 mb-1.5 pb-1 border-b border-panel-border/60">
              {children}
            </h3>
          ),
          h4: ({ children }) => (
            <h4 className="text-xs sm:text-sm font-bold text-text mt-2 mb-1">
              {children}
            </h4>
          ),
          p: ({ children }) => (
            <p className="mb-2 last:mb-0 leading-relaxed text-sm text-text">
              {children}
            </p>
          ),
          ul: ({ children }) => (
            <ul className="list-disc list-inside space-y-1 mb-2 text-sm text-text pl-1">
              {children}
            </ul>
          ),
          ol: ({ children }) => (
            <ol className="list-decimal list-inside space-y-1 mb-2 text-sm text-text pl-1">
              {children}
            </ol>
          ),
          li: ({ children }) => (
            <li className="leading-snug text-sm">{children}</li>
          ),
          strong: ({ children }) => (
            <strong className="font-bold text-text">{children}</strong>
          ),
          em: ({ children }) => (
            <em className="italic text-text-dim text-xs block my-1">
              {children}
            </em>
          ),
          code: ({ children }) => (
            <code className="bg-slate-100 text-slate-800 px-1.5 py-0.5 rounded text-xs font-mono border border-slate-200">
              {children}
            </code>
          ),
        }}
      >
        {content}
      </ReactMarkdown>
    </div>
  );
};
