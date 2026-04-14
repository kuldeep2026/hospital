let mode = "login";
let role = "user";

// MODE SWITCH (Login / Signup)
function switchMode(selectedMode, event) {
    mode = selectedMode;

    document.querySelectorAll(".toggle button").forEach(btn => btn.classList.remove("active"));
    event.target.classList.add("active");

    document.getElementById("nameField").style.display = (mode === "signup") ? "block" : "none";
    document.getElementById("confirmField").style.display = (mode === "signup") ? "block" : "none";

    // also update doctor fields visibility
    document.getElementById("doctorFields").style.display =
        (role === "doctor" && mode === "signup") ? "block" : "none";

    document.getElementById("doctorNote").style.display =
        (role === "doctor" && mode === "signup") ? "block" : "none";

    updateButton();
}

// ROLE SWITCH (User / Doctor / Admin)
function switchRole(selectedRole, event) {
    role = selectedRole;

    document.querySelectorAll(".roles button").forEach(btn => btn.classList.remove("active"));
    event.target.classList.add("active");

    const info = {
        user: "Access symptom analysis and find doctors",
        doctor: "Manage your profile and patient consultations",
        admin: "Manage users, doctors, and system settings"
    };

    document.getElementById("infoText").innerText = info[role];

    document.getElementById("doctorFields").style.display =
        (role === "doctor" && mode === "signup") ? "block" : "none";

    document.getElementById("doctorNote").style.display =
        (role === "doctor" && mode === "signup") ? "block" : "none";

    updateButton();
}

// BUTTON TEXT UPDATE
function updateButton() {
    const btn = document.getElementById("submitBtn");

    if (mode === "login") {
        btn.innerText = `Sign In as ${capitalize(role)}`;
    } else {
        btn.innerText = `Create ${capitalize(role)} Account`;
    }
}
function increaseCount() {
    let count = localStorage.getItem("analysisCount");

    if (count === null) {
        count = 0;
    }

    count = parseInt(count) + 1;

    localStorage.setItem("analysisCount", count);
}

window.onload = function () {
    let count = localStorage.getItem("analysisCount");

    if (count === null) {
        count = 0;
    }

    document.getElementById("analysisCount").innerText = count;
};
function showDoctors() {
    document.getElementById("doctorPopup").style.display = "block";
}

function closePopup() {
    document.getElementById("doctorPopup").style.display = "none";
}
// MAIN AUTH FUNCTION (🔥 NEW)
function handleAuth() {

    let email = document.getElementById("email").value;
    let nameInput = document.getElementById("nameField").value;
    let password = document.getElementById("password").value;
    let confirmPassword = document.getElementById("confirmPassword").value;

    // 🔥 NEW: Doctor Experience (only if exists)
    let experienceInput = document.getElementById("experienceInput")?.value || "";

    if(email === ""){
        alert("Enter email");
        return;
    }

    // 🔥 PASSWORD CHECK (ONLY FOR SIGNUP)
    if(mode === "signup"){
        if(password !== confirmPassword){
            alert("Passwords do not match");
            return;
        }
    }

    let name;

    if(mode === "signup"){
        if(nameInput === ""){
            alert("Enter name");
            return;
        }
        name = nameInput;
    } else {
        name = email.split("@")[0];
    }

    // ✅ STORE EVERYTHING
    localStorage.setItem("userData", JSON.stringify({
        name: name,
        role: role,
        experience: experienceInput
    }));

    // 🔥 ROLE BASED REDIRECTION
    if(role === "user"){
        window.location.href = "user_dashboard.html";
    }
    else if(role === "doctor"){
        window.location.href = "doctor_dashboard.html";
    }
    else if(role === "admin"){
        window.location.href = "admin_dashboard.html";
    }
}
// HELPER
function capitalize(word) {
    return word.charAt(0).toUpperCase() + word.slice(1);
}
localStorage.setItem("userData", JSON.stringify({
    name: name,
    experience: experience
}));