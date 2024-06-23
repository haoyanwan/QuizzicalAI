/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      backgroundImage: {
        'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
        'gradient-conic':
          'conic-gradient(from 180deg at 50% 50%, var(--tw-gradient-stops))',
      },
      colors: {
        'accent-1': '#333',
        'accent-p': "#00457C",
        'accent-2': '#666',
        'accent-3': '#999',
        'accent-4': '#ccc',
        'accent-5': '#eee',
        'accent-6': '#f3f3f3',
        'accent-7': '#f5f5f5',
        'accent-8': '#f7f7f7',
        'accent-9': '#fafafa',
        'accent-10': '#fcfcfc',
        'accent-11': '#fefefe',
        'accent-12': '#fff',
      }
    },
    fontFamily:{
      nacelle: ['Nacelle', 'sans-serif'],
    }
  },
  plugins: [],
}
