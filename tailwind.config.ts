import type { Config } from "tailwindcss";

export default {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        background: "var(--background)",
        foreground: "var(--foreground)",
      },
      gridTemplateColumns: {
        '21': 'repeat(21, minmax(0, 1fr))',
        '31': 'repeat(31, minmax(0, 1fr))',
        '51': 'repeat(51, minmax(0, 1fr))'
      },
    },
  },
  safelist: [
    'grid-cols-21',
    'grid-cols-31',
    'grid-cols-51',
  ],
  plugins: [],
} satisfies Config;
