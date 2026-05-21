/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx}",
    "./components/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        surface:  "#0f1117",
        panel:    "#161b27",
        card:     "#1c2333",
        input:    "#202840",
        border:   "#2d3650",
        accent:   "#5b8dee",
        "accent-h": "#4070d4",
        muted:    "#6b7599",
        dim:      "#404868",
        success:  "#3ecf8e",
        danger:   "#f87171",
      },
      fontFamily: {
        sans: ["Inter", "system-ui", "sans-serif"],
        mono: ["'IBM Plex Mono'", "monospace"],
      },
      keyframes: {
        fadeUp:  { "0%": { opacity: "0", transform: "translateY(6px)" }, "100%": { opacity: "1", transform: "translateY(0)" } },
        fadeIn:  { "0%": { opacity: "0" }, "100%": { opacity: "1" } },
        blink:   { "0%,100%": { opacity: "0.2" }, "50%": { opacity: "1" } },
      },
      animation: {
        "fade-up": "fadeUp 0.25s ease both",
        "fade-in": "fadeIn 0.2s ease both",
        "blink":   "blink 1.2s ease infinite",
      },
    },
  },
  plugins: [],
};
