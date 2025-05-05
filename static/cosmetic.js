document.querySelector('#addFavoriteForm').addEventListener('submit', addFavorite)
document.querySelector('#closeModal').addEventListener('click', closeModal);
var modal;

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

    modal.querySelector("input[name='image']").value = image;
    modal.querySelector("input[name='name']").value = name;
    modal.querySelector("input[name='description']").value = description;
    modal.querySelector("input[name='type']").value = type;
    modal.querySelector("input[name='rarity']").value = rarity;
    modal.querySelector("input[name='series']").value = series;
    modal.querySelector("input[name='set']").value = set;
    modal.querySelector("input[name='introduction']").value = introduction;

    modal.style.display = "block";
}

function closeModal(){
    modal.style.display='none';
}

function addFavorite(event){
    event.preventDefault();

    var form = event.target;
    var formData = new FormData(form);

    fetch('/addFavorite', {
        method: 'POST',
        body: formData
    }).then(function(response) {
        if (response.ok) {
            document.getElementById('myModal').style.display = 'none';
        }
    });
}