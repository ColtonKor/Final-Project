document.querySelector('#addFavoriteForm').addEventListener('submit', addFavorite);
document.querySelector('#closeModal').addEventListener('click', closeModal);

let modal;

function openModal(cardElement) {
    const imgElement = cardElement.querySelector('img');

    const title = imgElement.dataset.title;
    const salePrice = imgElement.dataset.saleprice;
    const normalPrice = imgElement.dataset.normalprice;
    const thumb = imgElement.dataset.thumb;
    const steamAppID = imgElement.dataset.steamid;

    modal = document.getElementById("myModal");

    modal.querySelector(".modal-image").src = thumb;
    modal.querySelector(".modal-title").textContent = title;
    modal.querySelector(".modal-price").textContent = `Sale Price: $${salePrice}`;
    modal.querySelector(".modal-normal").textContent = `Normal Price: $${normalPrice}`;
    modal.querySelector(".modal-steamid").textContent = `Steam App ID: ${steamAppID}`;

    modal.querySelector("input[name='title']").value = title;
    modal.querySelector("input[name='salePrice']").value = salePrice;
    modal.querySelector("input[name='normalPrice']").value = normalPrice;
    modal.querySelector("input[name='thumb']").value = thumb;
    modal.querySelector("input[name='steamAppID']").value = steamAppID;

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