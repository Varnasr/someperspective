/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./index.html', './app.js', './downloads/*.html'],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        primary: '#3b82f6',
        secondary: '#8b5cf6',
        accent: '#f59e0b'
      }
    }
  },
  plugins: []
}
