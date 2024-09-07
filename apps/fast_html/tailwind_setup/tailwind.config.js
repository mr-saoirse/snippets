/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'class',
  content: ['./*.html'],
  theme: {
    extend: {
      colors: {
        // Define colors for multiple themes
        light: {
          primary: '#3490dc',
          background: '#ffffff',
          text: '#000000',
        },
        dark: {
          primary: '#6574cd',
          background: '#1a202c',
          text: '#ffffff',
        },
        offwhite: {
          primary: '#ff6600',
          background: '#f5f5f5',
          text: '#333333',
        },
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
  ],
}

