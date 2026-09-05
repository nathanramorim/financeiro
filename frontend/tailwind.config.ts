import type { Config } from "tailwindcss";

export default {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        bg: "var(--bg)",
        panel: "var(--panel)",
        "panel-border": "var(--panel-border)",
        "panel-border-strong": "var(--panel-border-strong)",
        text: "var(--text)",
        "text-dim": "var(--text-dim)",
        primary: {
          DEFAULT: "var(--primary)",
          hover: "var(--primary-hover)",
        },
        success: {
          DEFAULT: "var(--success)",
          bg: "var(--success-bg)",
        },
        warning: {
          DEFAULT: "var(--warning)",
          bg: "var(--warning-bg)",
        },
        danger: {
          DEFAULT: "var(--danger)",
          bg: "var(--danger-bg)",
        },
        accent: {
          indigo: "var(--accent-indigo)",
          violet: "var(--accent-violet)",
          "blue-soft": "var(--accent-blue-soft)",
          "blue-softer": "var(--accent-blue-softer)",
        }
      },
      fontFamily: {
        sans: ["var(--font-montserrat)", "system-ui", "sans-serif"],
      },
      borderRadius: {
        card: "12px",
        btn: "8px",
        pill: "9999px",
      }
    },
  },
  plugins: [],
} satisfies Config;
