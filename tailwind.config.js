/**
 * Tailwind config for the someperspective static site.
 *
 * The site is a single hand-edited index.html served as-is by GitHub Pages.
 * This config replaces the former runtime CDN build (cdn.tailwindcss.com) with
 * a precompiled, purged stylesheet (styles.css). Edit index.html as usual; the
 * GitHub Actions deploy recompiles styles.css before publishing, and the
 * validate workflow guards against a stale committed copy.
 *
 * Purge note: Tailwind only keeps classes it finds as literal tokens while
 * scanning `content`. Every class in index.html — including the ternaries in
 * Alpine :class bindings and the class strings assigned in JS — is a literal,
 * so all are detected. The safelist below is belt-and-suspenders for the
 * handful of utility classes that are only ever assigned from JavaScript.
 */
module.exports = {
  content: ["./index.html"],
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        primary: "#3b82f6",
        secondary: "#8b5cf6",
        accent: "#f59e0b",
      },
    },
  },
  safelist: [
    // Trajectory verdict colours (assigned in JS, see index.html updateTrajectory)
    "text-emerald-600", "dark:text-emerald-400",
    "text-red-600", "dark:text-red-400",
    "text-amber-600", "dark:text-amber-400",
    "text-gray-500",
    // Toast notification (className assigned in JS)
    "fixed", "bottom-6", "left-1/2", "-translate-x-1/2", "bg-green-600",
    "text-white", "px-6", "py-3", "rounded-xl", "shadow-lg", "z-[100]",
    "text-sm", "font-medium",
  ],
};
