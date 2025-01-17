/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./components/**/*.{js,vue,ts}",
        "./layouts/**/*.vue",
        "./pages/**/*.vue",
        "./pages/*.vue",
        "./plugins/**/*.{js,ts}",
        "./app.vue",
        "./error.vue",
    ],
    theme: {
        extend: {
            colors: {
                primary: "#635FC7",
                primaryLight: "#F4F7FD",
                mediumGray: "#828FA3",
                darkGray: "#2B2C37",
                darkLines: "#3E3F4E",
                darkBackground: "#20212C"
            },
            letterSpacing: {
                "theme": "2.4px",
            },
            lineHeight: {
                "body": "23px",
            },
            fontSize: {
                "body": "13px",
                "large": "18px"
            }
        },
        fontFamily: {
            sans: ['Plus Jakarta Sans', 'sans-serif'],
            serif: ['Plus Jakarta Sans', 'sans-serif'],
            code: ['Fira Code', 'monospace'],
        },
    },
    plugins: [],
}

