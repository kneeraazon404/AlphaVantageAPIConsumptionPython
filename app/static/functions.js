// <script src="https://kit.fontawesome.com/c755a477ee.js" crossorigin="anonymous"></script>

const setTheme = theme => {
    document.documentElement.className = theme;
    localStorage.setItem('theme', theme);
}

const getTheme = () => {
    const theme = localStorage.getItem('theme');
    theme && setTheme(theme);
}
