// GET STORED USER DATA
let user = JSON.parse(localStorage.getItem("userData"));

// EXPERIENCE
if (user && user.experience) {
    document.getElementById("experience").innerText = user.experience + " Years";
} else {
    document.getElementById("experience").innerText = "—";
}

// PATIENTS (dummy for now)
document.getElementById("patients").innerText = "0";