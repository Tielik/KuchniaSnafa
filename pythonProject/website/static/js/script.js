let wybrane = [];
let formField = document.getElementById('formField');
document.getElementById("btnGotowe").style.display="none";
function podajIlosc(idProduktu, nazwaProduktu) {
    console.log(wybrane);
    if(wybrane.includes(idProduktu)) {
        return false;
    }
    else {
        wybrane.push(idProduktu);
        document.getElementById("btnGotowe").style.display = "block";

        let pole = document.createElement("div");
        pole.setAttribute("id", "pole");

        let nazwa = document.createElement("label");
        nazwa.setAttribute("id", "nazwaProduktu");
        nazwa.setAttribute("for", idProduktu);
        nazwa.innerHTML = nazwaProduktu;

        let ilosc = document.createElement("input");
        ilosc.setAttribute("type", "text");
        ilosc.setAttribute("id", idProduktu);
        ilosc.setAttribute("name",idProduktu);
        ilosc.setAttribute("style","display:none;");

        pole.append(document.createElement("br"));
        pole.append(nazwa);
        pole.append(ilosc);

        formField.append(pole);
    }
}
