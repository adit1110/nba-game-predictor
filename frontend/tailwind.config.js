/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./index.html', './src/**/*.{js,jsx,ts,tsx}'],
  theme: {
    extend: {
      fontFamily: {
        title: ['"Bebas Neue"', 'cursive'],
        sans: ['"Poppins"', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
