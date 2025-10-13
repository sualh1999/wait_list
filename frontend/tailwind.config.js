/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}', // Also check root components
    './app/**/*.{js,ts,jsx,tsx,mdx}', // Also check root app
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
