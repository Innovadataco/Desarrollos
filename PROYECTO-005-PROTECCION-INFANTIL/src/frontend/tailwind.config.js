/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        primary: "#0d9488",
        "primary-dark": "#0f766e",
      },
    },
  },
  plugins: [],
};