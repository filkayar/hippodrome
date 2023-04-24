let addCouple = document.querySelector(".add-couple");
let tbody = document.getElementById("list-couples");

function addListenerRemove() {
    let rem_couple = document.getElementById("list-couples");
    rem_couple.addEventListener('click', (e)=>{
        if (e.target.className === "fa-solid fa-xmark") {
            e.target.parentElement.parentElement.remove();
            refreshCouples();
        }
    });
}
addListenerRemove();

addCouple.addEventListener('click', (e)=>{
    let d, tag_i, tag_input, tag_d, tag_icon;
    let c = tbody.querySelectorAll("tr").length - 1;

    let tag_tr = document.createElement("tr");
    for (let i = 0; i < 6; i++) {
        let t = document.createElement("td");
        switch (i) {
            case 0:
                d = document.createElement("div");
                d.className = "link";

                tag_i = document.createElement("i");
                tag_i.className = "fa-solid fa-link";

                tag_input = document.createElement("input");
                tag_input.id = "couple-"+c.toString()+`-`+i.toString();
                tag_input.setAttribute("name", "couple-"+c.toString()+`-`+i.toString());
                tag_input.setAttribute("type", "number");
                tag_input.className = "couple-input";

                tag_d = document.createElement("div");
                tag_d.className = "link-input";
                tag_d.setAttribute("for", "table_horses");

                d.append(tag_i);
                d.append(tag_input);
                d.append(tag_d);
                t.append(d);
                break;
            case 1:
                d = document.createElement("div");
                d.className = "link";

                tag_i = document.createElement("i");
                tag_i.className = "fa-solid fa-link";

                tag_input = document.createElement("input");
                tag_input.id = "couple-"+c.toString()+`-`+i.toString();
                tag_input.setAttribute("name", "couple-"+c.toString()+`-`+i.toString());
                tag_input.setAttribute("type", "number");
                tag_input.className = "couple-input";

                tag_d = document.createElement("div");
                tag_d.className = "link-input";
                tag_d.setAttribute("for", "table_jokey");

                d.append(tag_i);
                d.append(tag_input);
                d.append(tag_d);
                t.append(d);
                break;
            case 2:
                tag_input = document.createElement("input");
                tag_input.setAttribute("name", "couple-"+c.toString()+`-`+i.toString());
                tag_input.className = "input-text  couple-input";
                tag_input.setAttribute("type", "number");

                t.append(tag_input);
                break;
            case 3:
                tag_input = document.createElement("input");
                tag_input.setAttribute("name", "couple-"+c.toString()+`-`+i.toString());
                tag_input.className = "input-text couple-input";
                tag_input.setAttribute("type", "time");

                t.append(tag_input);
                break;
            case 4:
                tag_icon = document.createElement("i");
                tag_icon.className = "fa-solid fa-xmark";

                t.append(tag_icon);
                break;
        }
        tag_tr.append(t);
    } 

    tbody.append(tag_tr);
    addListenerLinks();
    addListenerRemove();
});