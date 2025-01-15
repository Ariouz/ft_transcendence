class TournamentDetailsManager {
  constructor() {
    this.tournamentData = null;
    this.session = null;
    this.participantKey = [];
    this.loading = false;

    // DOM Elements
    this.elements = {
      joinButton: document.getElementById("joinButtonContainer"),
      tournamentInfo: document.getElementById("tournamentInfo"),
      participantsSection: document.getElementById("participantsSection"),
      participantsList: document.getElementById("participantsList"),
      matchesSection: document.getElementById("matchesSection"),
      nextRoundSection: document.getElementById("nextRoundSection"),
      loadingSpinner: document.getElementById("loadingSpinner"),
      nextRoundButton: document.getElementById("nextRoundButton"),
    };

    this.init();
  }

  async init() {
    this.showLoading(true);
    const urlParams = new URLSearchParams(window.location.search);
    const tournamentId = urlParams.get("id");

    if (tournamentId) {
      await this.loadTournamentData(tournamentId);
      this.setupEventListeners();
    }
  }

  setupEventListeners() {
    this.elements.nextRoundButton.addEventListener("click", () =>
      this.handleNextGame()
    );
  }

  async loadTournamentData(tournamentId) {
    try {
      const response = await fetchTournamentInfo(tournamentId);
      this.tournamentData = response;
      await this.initializeData(response);
      this.render();
    } catch (error) {
      console.error("Error loading tournament:", error);
    } finally {
      this.showLoading(false);
    }
  }

  async initializeData(data) {
    // Simulate session for demo - replace with actual session management
    this.session = { user: { id: "user123" } };

    const userJoined = data.particpants?.find(
      (p) => p.user_id === this.session.user.id
    );
    const canJoin = data.detail[0].numberOfPlayers > data.particpants?.length;

    this.updateJoinState(userJoined, canJoin);
    await this.handleMatchmaking(data);
  }

  async handleMatchmaking(data) {
    if (data.detail[0].numberOfPlayers === data.particpants?.length) {
      this.showLoading(true);
      const defaultRoundID =
        data.detail[0].round > 0 ? data.detail[0].round : 1;
      await this.createMatches(data.detail[0].id, defaultRoundID);
    }
  }

  async createMatches(tournamentId, roundId) {
    try {
      let matchData = await createMatchMakingTournament(tournamentId, roundId);

      if (!matchData.particpants) {
        await createMatchMaking(tournamentId, roundId);
        matchData = await createMatchMakingTournament(tournamentId, roundId);
      }

      this.handleMatchData(matchData);
    } finally {
      this.showLoading(false);
    }
  }

  handleMatchData(matchData) {
    if (matchData.particpants?.length > 0) {
      this.updateParticipantKeys(matchData.particpants);
      this.renderMatches(matchData.particpants);
    }
  }

  updateParticipantKeys(participants) {
    this.participantKey = participants.reduce((keys, participant) => {
      const playerKeys = Object.keys(participant).filter(
        (key) => key.includes("player") && key.includes("_name")
      );
      return [...new Set([...keys, ...playerKeys])];
    }, []);
  }

  render() {
    this.renderTournamentInfo();
    this.renderParticipants();
    this.updateJoinButton();
  }

  renderTournamentInfo() {
    if (!this.tournamentData?.detail?.length) return;

    const tournament = this.tournamentData.detail[0];
    this.elements.tournamentInfo.innerHTML = `
            <div class="tournament-card">
                <h5 class="fw-bold">${tournament.name}</h5>
                <p>Number of Players: ${tournament.numberOfPlayers || "--"}</p>
                <p>Points Per Game: ${tournament.pointsPerGame || "--"}</p>
                <p>Timer: ${tournament.timer || "--"}</p>
            </div>
        `;
  }

  renderParticipants() {
    const participants = this.tournamentData?.particpants;
    if (!participants?.length) return;

    this.elements.participantsSection.classList.remove("d-none");
    this.elements.participantsList.innerHTML = participants
      .map(
        (p, i) => `
                <div class="participant-item">
                    ${i + 1}. ${p.user_name}
                </div>
            `
      )
      .join("");
  }

  renderMatches(matches) {
    this.elements.matchesSection.classList.remove("d-none");
    this.elements.matchesSection.innerHTML = matches
      .map((match, index) => this.createMatchCard(match, index))
      .join("");
  }

  createMatchCard(match, index) {
    return `
            <div class="match-card">
                ${
                  index === 0
                    ? `<h4 class="round-header">Round: ${match.round_id}</h4>`
                    : ""
                }
                ${this.participantKey
                  .map((key) => {
                    const playerKey = key.replace("_name", "");
                    const isWinner = match[playerKey] === match.winner;
                    return `
                        <div class="d-flex justify-content-between align-items-center">
                            <div>
                                ${match[key]}
                                ${
                                  isWinner
                                    ? '<span class="winner-tag">WINNER</span>'
                                    : ""
                                }
                            </div>
                            ${
                              match[playerKey] === this.session.user.id
                                ? `<a href="#" class="join-link" data-room="${match.linkToJoin}">Join Game</a>`
                                : ""
                            }
                        </div>
                    `;
                  })
                  .join("")}
            </div>
        `;
  }

  updateJoinButton() {
    const canJoin =
      this.tournamentData?.detail[0].numberOfPlayers >
      this.tournamentData?.particpants?.length;

    if (!canJoin) return;

    const isParticipant = this.tournamentData?.particpants?.some(
      (p) => p.user_id === this.session.user.id
    );

    this.elements.joinButton.innerHTML = `
            <button class="btn btn-primary" onclick="${
              isParticipant ? "leaveTournament()" : "joinTournament()"
            }">
                ${isParticipant ? "Leave" : "Join"}
            </button>
        `;
  }

  showLoading(show) {
    this.loading = show;
    this.elements.loadingSpinner.classList.toggle("d-none", !show);
  }
}

// Initialize the tournament details manager
document.addEventListener("DOMContentLoaded", () => {
  new TournamentDetailsManager();
});
