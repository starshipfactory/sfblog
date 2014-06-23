domready(function() {
    var btn = document.querySelector(".menu-btn");
    var menu = document.querySelector(".nav-main");

    function toggleMenu(e) {
        menu.classList.toggle("expanded");
        e.preventDefault();
    }

    btn.addEventListener("click", toggleMenu, false);
});
