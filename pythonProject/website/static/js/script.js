let wybrane = [];
{% if skladnikiwybrane %}
{%for x in  in SkladnikiWybrane %}
let x={{x.id}}
if x!=null{
wybrane.push(x);
}
{%endfor%}
{%endif%}
let formfield = document.querySelector(".formfield");
document.querySelector(".btn-gotowe").style.display="none";
function wybierzSkladnik(idProduktu, nazwaProduktu) {
    if(wybrane.includes(idProduktu)) {
        return false;
    }
    else {
        wybrane.push(idProduktu);
        document.querySelector(".btn-gotowe").style.display = "block";

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
        btn.setAttribute("class", "btn-usun float-end btn btn-danger");
        btn.innerHTML = "Usuń";
        btn.onclick = () =>  {
            formfield.removeChild(pole);
            wybrane.splice(wybrane.indexOf(idProduktu), 1);
        }

        pole.append(document.createElement("br"));
        pole.append(nazwa);
        pole.append(ID);
        pole.append(btn);

        formfield.append(pole);
    }
}
function delete(produktid){

const index = wybrane.indexOf(produktid);

const x = myArray.splice(index, 1);
let pDoUsuniecia=document.getElementById(`$produktid}`);
pDoUsuniecia.remove();

}
//funkcja od usuwania
