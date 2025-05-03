document.querySelector('#ShowFortnite').addEventListener('click', OpenFortnite);
document.querySelector('#ShowSteam').addEventListener('click', OpenSteam);
document.querySelector('#closeModal').addEventListener('click', closeModal);
document.querySelector('#closeGameModal').addEventListener('click', closeModal);
var modal;

var is_fortnite = document.getElementById("hiddenTab").value === "1";
if(is_fortnite){
    document.getElementById("Steam").style.display = "none";
    document.getElementById("Fortnite").style.display = "flex";

    document.getElementById("ShowSteam").classList.remove("chosen-btn");
    document.getElementById("ShowSteam").classList.add("not-chosen-btn");

    document.getElementById("ShowFortnite").classList.remove("not-chosen-btn");
    document.getElementById("ShowFortnite").classList.add("chosen-btn");
} else {
    document.getElementById("Fortnite").style.display = "none";
    document.getElementById("Steam").style.display = "flex";

    document.getElementById("ShowFortnite").classList.remove("chosen-btn");
    document.getElementById("ShowFortnite").classList.add("not-chosen-btn");

    document.getElementById("ShowSteam").classList.remove("not-chosen-btn");
    document.getElementById("ShowSteam").classList.add("chosen-btn");
}


function OpenFortnite(){
    document.getElementById("Steam").style.display = "none";
    document.getElementById("Fortnite").style.display = "flex";

    document.getElementById("ShowSteam").classList.remove("chosen-btn");
    document.getElementById("ShowSteam").classList.add("not-chosen-btn");

    document.getElementById("ShowFortnite").classList.remove("not-chosen-btn");
    document.getElementById("ShowFortnite").classList.add("chosen-btn");
}


function OpenSteam(){
    document.getElementById("Fortnite").style.display = "none";
    document.getElementById("Steam").style.display = "flex";
    
    document.getElementById("ShowFortnite").classList.remove("chosen-btn");
    document.getElementById("ShowFortnite").classList.add("not-chosen-btn");

    document.getElementById("ShowSteam").classList.remove("not-chosen-btn");
    document.getElementById("ShowSteam").classList.add("chosen-btn");
}


function openModal(cardElement) {
    const imgElement = cardElement.querySelector('img');
    const name = imgElement.dataset.name;
    const description = imgElement.dataset.description;
    const image = imgElement.dataset.image;
    const type = imgElement.dataset.type;
    const rarity = imgElement.dataset.rarity;
    const series = imgElement.dataset.series;
    const set = imgElement.dataset.set;
    const introduction = imgElement.dataset.introduction;
    const id = imgElement.dataset.id;

    // Example modal logic
    modal = document.getElementById("myModal");
    modal.querySelector(".modal-image").src = image;
    modal.querySelector(".modal-title").textContent = name;
    modal.querySelector(".modal-description").textContent = description;
    modal.querySelector(".modal-type").textContent = type;
    modal.querySelector(".modal-rarity").textContent = rarity;
    modal.querySelector(".modal-series").textContent = series;
    modal.querySelector(".modal-set").textContent = set;
    modal.querySelector(".modal-introduction").textContent = introduction;
    modal.querySelector(".modal-introduction").textContent = id;

    modal.querySelector("input[name='id']").value = id;

    modal.style.display = "block";
}

function openGameModal(cardElement) {
    const imgElement = cardElement.querySelector('img');

    const title = imgElement.dataset.title;
    const salePrice = imgElement.dataset.saleprice;
    const normalPrice = imgElement.dataset.normalprice;
    const thumb = imgElement.dataset.thumb;
    const steamAppID = imgElement.dataset.steamid;
    const id = imgElement.dataset.id;

    modal = document.getElementById("myGameModal");

    modal.querySelector(".modal-image").src = thumb;
    modal.querySelector(".modal-title").textContent = title;
    modal.querySelector(".modal-price").textContent = `Sale Price: $${salePrice}`;
    modal.querySelector(".modal-normal").textContent = `Normal Price: $${normalPrice}`;
    modal.querySelector(".modal-steamid").textContent = `Steam App ID: ${steamAppID}`;


    modal.querySelector("input[name='id']").value = id;    

    modal.style.display = "block";
}

function closeModal(){
    modal.style.display='none';
}