let formField = document.getElementById('formField');

let id = 0;

function podajIlosc(produkt) {
    id += 1;

    let pole = document.createElement("div");
    pole.setAttribute("id", "pole");

    let nazwaProduktu = document.createElement("label");
    nazwaProduktu.setAttribute("id", "nazwaProduktu");
    nazwaProduktu.setAttribute("for", id)
    nazwaProduktu.innerHTML = produkt;

    pole.append(nazwaProduktu)

    let ilosc = document.createElement("input");
    ilosc.setAttribute("type", "text");
    ilosc.setAttribute("id", id);
    ilosc.setAttribute("placeholder", "Podaj ilość");

    pole.append(ilosc);

    formField.append(pole);
}

function wyswietlPrzepisy() {
    let snaf = document.querySelector(".przepisySnafa");
    let line = document.createElement('hr');
    snaf.append(line);
    let przepisy = document.createElement("p");
    przepisy.innerHTML = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
    snaf.append(przepisy);
    const button = document.getElementById("gotoweBtn")
    button.setAttribute("disabled", "");
}