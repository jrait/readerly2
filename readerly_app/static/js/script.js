$('body').toggleClass(localStorage.toggled);

function darkLight() {
    if (localStorage.toggled != 'dark_mode') {
        $('body').toggleClass('dark_mode', true);
        localStorage.toggled = 'dark_mode';
    } else {
        $('body').toggleClass('dark_mode', false);
        localStorage.toggled = '';
    }
}