/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      colors: {
        ink: '#162329',
        paper: '#f5f7f4',
        mint: '#dcefe8',
        fern: '#2f6d5a',
        coral: '#d8785d',
        line: '#d8e0dc',
      },
      fontFamily: {
        display: ['DM Sans', 'sans-serif'],
        body: ['Source Sans 3', 'sans-serif'],
      },
      boxShadow: {
        panel: '0 18px 45px rgba(25, 58, 50, 0.08)',
      },
    },
  },
  plugins: [],
}
