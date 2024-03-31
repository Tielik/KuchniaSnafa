// function sprawdzHaslo(){
//     document.querySelector(".container").style.display = "none";
//     let formHaslo = document.createElement("form");
//     formHaslo.setAttribute("method", "get");
//     formHaslo.setAttribute("action", "");

//     let podaj = document.createElement("label");
//     podaj.setAttribute("id", "podaj");
//     podaj.innerHTML = "Wprowadź hasło";

//     body = document.querySelector("body");

//     let haslo = document.createElement("input");
//     haslo.setAttribute("type", "text");

//     let submitHaslo = document.createElement("input");
//     submitHaslo.setAttribute("type", "submit");
//     submitHaslo.setAttribute("value", "Submit");
    
//     formHaslo.appendChild(podaj)  
//     formHaslo.appendChild(haslo);
//     formHaslo.appendChild(submitHaslo);
//     body.appendChild(formHaslo);

//     if(haslo.innerHTML != ""){
//         if(haslo.innerHTML != "snaf")
//             sprawdzHaslo()
//         else{
//             body.removeChild(formHaslo);
//             document.querySelector(".container").style.display = "block";
//         }
//     }
// }

// window.onload = sprawdzHaslo();

let formField = document.getElementById('formField');

let id = 0;

function podajProdukt(kategoria) {
    document.getElementById("btnGotowe").style.display = "block";

    id += 1;

    let pole = document.createElement("div");
    pole.setAttribute("id", "pole");

    let nazwaProduktu = document.createElement("label");
    nazwaProduktu.setAttribute("id", "nazwaProduktu");
    nazwaProduktu.setAttribute("for", id)
    nazwaProduktu.innerHTML = kategoria + ":";

    pole.appendChild(nazwaProduktu)

    let produkt = document.createElement("input");
    produkt.setAttribute("type", "text");
    produkt.setAttribute("id", id);
    produkt.setAttribute("class", "float-right");
    produkt.setAttribute("placeholder", "Wprowadź nazwę produktu");

    pole.appendChild(produkt);

    formField.appendChild(pole);
}

function wyswietlPrzepisy() {
    let snaf = document.querySelector(".przepisySnafa");
    let line = document.createElement('hr');
    snaf.appendChild(line);
    let przepisy = document.createElement("p");
    przepisy.innerHTML = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
    snaf.appendChild(przepisy);
    const button = document.getElementById("btnGotowe")
    button.setAttribute("disabled", "");
}