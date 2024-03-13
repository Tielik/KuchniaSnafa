function podajIlosc(produkt) {
    let form = document.createElement("form");
    form.setAttribute("method", "post");
    form.setAttribute("action", "");
    form.innerHTML = produkt;

    let ilosc = document.createElement("input");
    ilosc.setAttribute("type", "text");
    ilosc.setAttribute("id", "ilosc");
    ilosc.setAttribute("placeholder", "Podaj ilość");

    form.append(ilosc);

    let down = document.querySelector(".iloscForm");
    down.appendChild(form);
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