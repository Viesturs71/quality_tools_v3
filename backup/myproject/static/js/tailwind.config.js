module.exports = {
  content: [
    "../templates/**/*.html",
    "../**/templates/**/*.html",
  ],
  theme: {
    extend: {
      colors: {
        primary: '#2563eb',   /* blue-600 */
        secondary: '#e5e7eb', /* gray-200 */
        accent: '#6366f1',    /* indigo-500 */
        success: '#10b981',   /* green-500 */
        warning: '#f59e0b',   /* amber-500 */
        danger: '#ef4444',    /* red-500 */
        info: '#0ea5e9',      /* sky-500 */
      },
      fontFamily: {
        'serif': ['"Times New Roman"', 'serif'],
      }
    }
  },
  plugins: [],
}
