function changeTheme() {
    var theme = document.getElementById("theme-style");

    if (theme.getAttribute("href").includes("light.css")) {
        theme.setAttribute("href", "/static/dark.css");
    } else {
        theme.setAttribute("href", "/static/light.css");
    }
}
