document.querySelector('#ShowFortnite').addEventListener('click', OpenFortnite);
document.querySelector('#ShowSteam').addEventListener('click', OpenSteam);
document.querySelector('#closeModal').addEventListener('click', closeModal);
document.querySelector('#closeGameModal').addEventListener('click', closeModal);
var modal;

var is_fortnite = document.getElementById("hiddenTab").value === "1";
if(is_fortnite){
    document.getElementById("Steam").style.display = "none";
    document.getElementById("Fortnite").style.display = "flex";
    document.getElementById("emailButton").style.display = "block";

    document.getElementById("ShowSteam").classList.remove("chosen-btn");
    document.getElementById("ShowSteam").classList.add("not-chosen-btn");

    document.getElementById("ShowFortnite").classList.remove("not-chosen-btn");
    document.getElementById("ShowFortnite").classList.add("chosen-btn");
} else {
    document.getElementById("Fortnite").style.display = "none";
    document.getElementById("Steam").style.display = "flex";
    document.getElementById("emailButton").style.display = "none";

    document.getElementById("ShowFortnite").classList.remove("chosen-btn");
    document.getElementById("ShowFortnite").classList.add("not-chosen-btn");

    document.getElementById("ShowSteam").classList.remove("not-chosen-btn");
    document.getElementById("ShowSteam").classList.add("chosen-btn");
}


function OpenFortnite(){
    document.getElementById("Steam").style.display = "none";
    document.getElementById("Fortnite").style.display = "flex";
    document.getElementById("emailButton").style.display = "block";

    document.getElementById("ShowSteam").classList.remove("chosen-btn");
    document.getElementById("ShowSteam").classList.add("not-chosen-btn");

    document.getElementById("ShowFortnite").classList.remove("not-chosen-btn");
    document.getElementById("ShowFortnite").classList.add("chosen-btn");

    document.getElementById("hiddenTab").value = 1;
}


function OpenSteam(){
    document.getElementById("Fortnite").style.display = "none";
    document.getElementById("Steam").style.display = "flex";
    document.getElementById("emailButton").style.display = "none";
    
    document.getElementById("ShowFortnite").classList.remove("chosen-btn");
    document.getElementById("ShowFortnite").classList.add("not-chosen-btn");

    document.getElementById("ShowSteam").classList.remove("not-chosen-btn");
    document.getElementById("ShowSteam").classList.add("chosen-btn");

    document.getElementById("hiddenTab").value = 2;
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
    modal.querySelector(".modal-introduction").textContent = `Release Date: ${introduction}`;

    modal.querySelector("input[name='id']").value = id;

    modal.style.display = "block";
}

function openGameModal(cardElement) {
    const imgElement = cardElement.querySelector('img');

    const title = imgElement.dataset.title;
    const thumb = imgElement.dataset.thumb;
    const genre = imgElement.dataset.genre;
    const description = imgElement.dataset.description;
    const platform = imgElement.dataset.platform;
    const publisher = imgElement.dataset.publisher;
    const developer = imgElement.dataset.developer;
    const release = imgElement.dataset.release;

    const id = imgElement.dataset.id;

    modal = document.getElementById("myGameModal");

    modal.querySelector("#imageDisplay").src = thumb;
    modal.querySelector("#titleDisplay").textContent = title;
    modal.querySelector("#descriptionDisplay").textContent = description;
    modal.querySelector("#genreDisplay").textContent = `Genre: ${genre}`;
    modal.querySelector("#platformDisplay").textContent = `Platform: ${platform}`;
    modal.querySelector("#publisherDisplay").textContent = `Publisher: ${publisher}`;
    modal.querySelector("#developerDisplay").textContent = `Developer: ${developer}`;
    modal.querySelector("#releaseDisplay").textContent = `Release Date: ${release}`;

    modal.querySelector("input[name='id']").value = id;

    modal.style.display = "block";
}

function closeModal(){
    modal.style.display='none';
}

function switchTab(tabIndex) {
    const url = new URL(window.location.href);
    url.searchParams.set('currentTab', tabIndex);
    window.history.replaceState(null, '', url);
}