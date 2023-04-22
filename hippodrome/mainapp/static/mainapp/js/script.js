document.getElementById("show-sidebar").addEventListener('click', function() {
    document.getElementById("sidebar").classList.add("active");
    document.getElementById("page-overlay").classList.add("active");
});

document.getElementById("page-overlay").addEventListener('mousedown', function(e) {
    e.target.classList.remove("active");
    document.getElementById("sidebar").classList.remove("active");
    if (document.getElementById("auth") !== null)
        document.getElementById("auth").classList.remove("active");
    let vs = document.getElementsByClassName("viborka");
    for (let i = 0; i < vs.length; i++) {
        vs[i].classList.remove("active");
        resetSearch(vs[i]);
    }
});