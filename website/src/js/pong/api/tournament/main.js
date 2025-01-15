// DOM Elements
const tournamentsList = document.getElementById("tournamentsList");
const tournamentModal = new bootstrap.Modal(
  document.getElementById("tournamentModal")
);
const tournamentForm = document.getElementById("tournamentForm");
const nameError = document.getElementById("nameError");
const pointsValue = document.getElementById("pointsValue");

// Event Listeners
document.getElementById("createTournamentBtn").addEventListener("click", () => {
  resetForm();
  tournamentModal.show();
});

document
  .getElementById("submitTournament")
  .addEventListener("click", handleSubmitData);

// Form handling
tournamentForm
  .querySelector('[name="gamePoint"]')
  .addEventListener("input", (e) => {
    pointsValue.textContent = e.target.value;
  });

function resetForm() {
  tournamentForm.reset();
  nameError.textContent = "";
  pointsValue.textContent = "0";
}

// Input validation
function isNumber(event) {
  const charCode = event.which ? event.which : event.keyCode;
  if (charCode > 31 && (charCode < 48 || charCode > 57) && charCode !== 46) {
    event.preventDefault();
    return false;
  }
  return true;
}

// Add number validation to relevant inputs
["numberOfPlayer", "timer"].forEach((fieldName) => {
  tournamentForm
    .querySelector(`[name="${fieldName}"]`)
    .addEventListener("keydown", isNumber);
});

// Form submission
async function handleSubmitData() {
  const formData = new FormData(tournamentForm);
  const tournamentData = {
    name: formData.get("name"),
    numberOfPlayers: formData.get("numberOfPlayer"),
    isPrivate: formData.get("isPrivate") === "on",
    difficultyLevel: formData.get("gameLevel"),
    pointsPerGame: parseInt(formData.get("gamePoint")),
    timer: parseInt(formData.get("timer")),
    powerUps: formData.get("powerUps") === "on",
  };

  if (!tournamentData.name) {
    nameError.textContent = "Required field";
    return;
  }

  try {
    await addTournamentData(tournamentData);
    tournamentModal.hide();
    fetchAndDisplayTournaments();
  } catch (error) {
    console.error("Error:", error);
    nameError.textContent = "Failed to add tournament";
  }
}

// Tournament list handling
function createTournamentElement(tournament, index) {
  const div = document.createElement("div");
  div.className = "tournament-item";
  div.innerHTML = `
        <span>${index + 1}. ${tournament.name}</span>
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M7 17L17 7"/>
            <path d="M7 7h10v10"/>
        </svg>
    `;
  div.addEventListener("click", () => handleSelectedData(tournament));
  return div;
}

function handleSelectedData(tournament) {
  window.location.href = `/tournaments/${tournament.id}`;
}

async function fetchAndDisplayTournaments() {
  const tournaments = await getTournamentData();
  tournamentsList.innerHTML = "";
  tournaments.forEach((tournament, index) => {
    tournamentsList.appendChild(createTournamentElement(tournament, index));
  });
}

// Initial load
fetchAndDisplayTournaments();
