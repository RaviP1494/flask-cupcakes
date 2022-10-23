const BASE_URL = '"http://localhost:5000/api'

ul = document.querySelector('#cupcake_list');
addForm = document.querySelector('#cupcake_add_form');

async function loadList(){
    let resp = await axios.get(`/api/cupcakes`);
    for (let li of ul.children){
        li.remove();
    }
    for (let cupcake of resp.data.cupcakes){
        let cupcakeElement = document.createElement('li');
        cupcakeElement.innerHTML = makeCakeHTML(cupcake);
        ul.append(cupcakeElement);
    }
}

function makeCakeHTML(cake){
    resp = `
    <div data-cake-id = ${cake.id}>
    <li>
    ${cake.flavor} cupcake: size ${cake.size} rated ${cake.rating }
    </li>
    <img src="${cake.image}">
    </div>`;

    return resp;
}

async function addCupcake(e){
    e.preventDefault();

    let flavor = document.querySelector("#flavor").value;
    let size = document.querySelector("#size").value;
    let rating = document.querySelector("#rating").value;
    let image = document.querySelector("#image").value;
    let resp = await axios.post(`/api/cupcakes`, {flavor,size,rating,image});
    await loadList();
}

document.addEventListener("DOMContentLoaded", loadList);
addForm.addEventListener("submit", addCupcake)