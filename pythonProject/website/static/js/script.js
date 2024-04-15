let wybrane = [];
let formField = document.querySelector(".formField");
document.querySelector(".btnGotowe").style.display="none";
function wybierzSkladnik(idProduktu, nazwaProduktu) {
    if(wybrane.includes(idProduktu)) {
        return false;
    }
    else {
        wybrane.push(idProduktu);
        document.querySelector(".btnGotowe").style.display = "block";

        let pole = document.createElement("div");
        pole.setAttribute("class", "pole");

        let nazwa = document.createElement("label");
        nazwa.setAttribute("id", "nazwaProduktu");
        nazwa.setAttribute("for", idProduktu);
        nazwa.innerHTML = nazwaProduktu;

        let ID = document.createElement("input");
        ID.setAttribute("type", "text");
        ID.setAttribute("id", idProduktu);
        ID.setAttribute("name",idProduktu);
        ID.setAttribute("style","display:none;");

        let btn = document.createElement("button");
        btn.setAttribute("type", "button");
        btn.setAttribute("class", "btnUsun float-end btn btn-danger");
        btn.innerHTML = "Usuń";
        btn.onclick = () =>  {
            formField.removeChild(pole);
            wybrane.splice(wybrane.indexOf(idProduktu), 1);
        }

        pole.append(document.createElement("br"));
        pole.append(nazwa);
        pole.append(ID);
        pole.append(btn);

        formField.append(pole);
    }
}
