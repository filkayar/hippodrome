let list_h = document.querySelectorAll(".horse-td");

let h_name  = document.getElementById("h-name");
let h_mast  = document.getElementById("h-mast");
let h_age   = document.getElementById("h-age");
let h_photo = document.getElementById("h-photo");

for(let i = 0; i < list_h.length; i++) {
    list_h[i].addEventListener('click', (e)=>{

        if (e.target.style["background-color"] === "") {
            let list_v = document.querySelectorAll("tr:has(#"+e.target.id+") td.no-display");
            let key = e.target.id.slice(1);
            filterHorses(key)

            h_name.innerHTML = e.target.innerHTML;
            h_name.href = list_v[3].innerHTML;
            h_photo.src = list_v[0].innerHTML;
            h_mast.innerHTML = list_v[1].innerHTML;
            h_age.innerHTML = list_v[2].innerHTML;
            e.target.style["background-color"] = "var(--color-link)";
            e.target.style["color"] = "var(--color-main)";
        } else {
            e.target.style["background-color"] = "";
            e.target.style["color"] = "";
            
            filterHorses(-1);
            h_name.href = "";
            h_name.innerHTML = "";
            h_photo.src = "";
            h_mast.innerHTML = "";
            h_age.innerHTML = "";
        }
            
    });
}

let list_hr = document.getElementsByClassName("horse-r");

function filterHorses(key) {
    let act_list = document.getElementsByClassName("horse-td");
    for(let j = 0; j < act_list.length; j++) {
        act_list[j].style["background-color"] = "";
        act_list[j].style["color"] = "";
    }
    for (let r = 0; r < list_hr.length; r++) {
        if (key !== -1) { 
            let r_key = list_hr[r].querySelector(".no-display").innerHTML;
            if (r_key !== key) {
                list_hr[r].style.display = "none";
            }
            else {
                list_hr[r].style.display = "table-row";
            }
        } else {
            list_hr[r].style.display = "table-row";
        }       
    }
}