let formField = document.getElementById('formField');

document.getElementById("btnGotowe").style.display="none";
function podajIlosc(idProduktu, nazwaProduktu) {
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
    pole.append(document.createElement("br"));

    formField.append(pole);
}

function wyswietlPrzepisy() {
    let snaf = document.querySelector(".przepisySnafa");
    let line = document.createElement('hr');
    snaf.append(line);
    let przepisy = document.createElement("p");
    przepisy.innerHTML = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
    snaf.append(przepisy);
    const button = document.getElementById("btnGotowe");
    button.setAttribute("disabled", "");
}