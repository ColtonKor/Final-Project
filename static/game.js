document.querySelector('#addFavoriteForm').addEventListener('submit', addFavorite);
document.querySelector('#closeModal').addEventListener('click', closeModal);

let modal;

function openModal(cardElement) {
    const imgElement = cardElement.querySelector('img');

    const title = imgElement.dataset.title;
    const thumb = imgElement.dataset.thumb;
    const genre = imgElement.dataset.genre;
    const description = imgElement.dataset.description;
    const platform = imgElement.dataset.platform;
    const publisher = imgElement.dataset.publisher;
    const developer = imgElement.dataset.developer;
    const release = imgElement.dataset.release;
    const url = imgElement.dataset.url;

    modal = document.getElementById("myModal");

    modal.querySelector("#imageDisplay").src = thumb;
    modal.querySelector("#titleDisplay").textContent = title;
    modal.querySelector("#descriptionDisplay").textContent = description;
    modal.querySelector("#genreDisplay").textContent = `Genre: ${genre}`;
    modal.querySelector("#platformDisplay").textContent = `Platform: ${platform}`;
    modal.querySelector("#publisherDisplay").textContent = `Publisher: ${publisher}`;
    modal.querySelector("#developerDisplay").textContent = `Developer: ${developer}`;
    modal.querySelector("#releaseDisplay").textContent = `Release Date: ${release}`;

    modal.querySelector("input[name='title']").value = title;
    modal.querySelector("input[name='thumb']").value = thumb;
    modal.querySelector("input[name='genre']").value = genre;
    modal.querySelector("input[name='description']").value = description;
    modal.querySelector("input[name='platform']").value = platform;
    modal.querySelector("input[name='publisher']").value = publisher;
    modal.querySelector("input[name='developer']").value = developer;
    modal.querySelector("input[name='release']").value = release;
    modal.querySelector("input[name='url']").value = url;

    modal.style.display = "block";
}

function closeModal() {
    if (modal) {
        modal.style.display = 'none';
    }
}

function addFavorite(event) {
    event.preventDefault();

    const form = event.target;
    const formData = new FormData(form);

    fetch('/addSteam', {
        method: 'POST',
        body: formData
    }).then(response => {
        if (response.ok) {
            closeModal();
        } else {
            alert("Failed to save favorite.");
        }
    });
}