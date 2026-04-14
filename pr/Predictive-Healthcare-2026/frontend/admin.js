let pendingCount = document.getElementById("pendingCount");

// INITIAL COUNT
updatePending();

// ADD EVENT LISTENERS
document.querySelectorAll(".approve").forEach(btn => {
    btn.addEventListener("click", function () {
        let card = btn.closest(".doctor-card");
        removeCard(card);
    });
});

document.querySelectorAll(".reject").forEach(btn => {
    btn.addEventListener("click", function () {
        let card = btn.closest(".doctor-card");
        removeCard(card);
    });
});

// REMOVE CARD FUNCTION
function removeCard(card) {
    card.style.opacity = "0";
    card.style.transform = "scale(0.9)";

    setTimeout(() => {
        card.remove();
        updatePending();
    }, 300);
}

// UPDATE COUNT
function updatePending() {
    let cards = document.querySelectorAll(".doctor-card").length;

    document.querySelector(".card:nth-child(3) h1").innerText = cards;
}