/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./core/**/*.{html,js}"],
  theme: {
    extend: {},
    container: {
      center: true,
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
  ],
}

