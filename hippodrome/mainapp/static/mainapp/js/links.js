let PO = document.getElementById("page-overlay");

function refreshCouples() {
    let couples = document.getElementsByClassName("couple-input");
    for (let i = 0; i < couples.length; i++) {
        couples[i].setAttribute("name", "couple-"+String(parseInt(i/4))+"-"+String(i%4));
    }
}


function addListenerLinks() {
    let links = document.getElementsByClassName("link-input");
    for (let l = 0; l < links.length; l++) {
        links[l].addEventListener("click", (e)=>{  
            let vib = document.getElementById(e.target.getAttribute("for"));

            vib.setAttribute("input", e.target.previousElementSibling.id);
            PO.classList.add("active");
            vib.classList.add("active");
        });
    }
}
addListenerLinks();


let photo = document.getElementById("race-photo");


let vs = document.getElementsByClassName("viborka");

for (let v = 0; v < vs.length; v++) {
    vs[v].addEventListener('click', (e)=>{
        if (e.target.tagName === "TD") {
            const key = e.target.id.split("-")[2];
            const att_url = e.target.getAttribute("url");
            const value = e.target.innerHTML;

            if (att_url !== '') {
                photo.src = att_url;
            }

            let vib = document.querySelector(".viborka:has(#" + e.target.id);
            let inp = document.getElementById(vib.getAttribute("input"));
            inp.nextElementSibling.innerHTML = value;
            inp.value = Number(key);

            vib.classList.remove("active");
            document.getElementById("page-overlay").classList.remove("active");
            resetSearch(vib);
        }
    });
}

let searches = document.querySelectorAll(".viborka input.input-text");
for( let i = 0; i < searches.length; i++) {
    searches[i].addEventListener('keyup', (e)=>{
        let v = e.target.parentElement.parentElement;
        let els = v.getElementsByClassName("el-v");
        for (let j = 0; j < els.length; j++) {
            if (!els[j].innerHTML.match(e.target.value)) {
                els[j].parentElement.style.display = "none";
            } else {
                els[j].parentElement.style.display = "table-row";
            }
        }
    })
}

function resetSearch(v) {
    let els = v.getElementsByClassName("el-v");
    let s = v.getElementsByClassName("input-text");
    s[0].value = "";
    for (let j = 0; j < els.length; j++) {
        els[j].parentElement.style.display = "table-row";
    }
}