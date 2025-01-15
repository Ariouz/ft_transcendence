// API Service functions

const BASE_URL = "https://localhost:8002";

export async function getTournamentData() {
  try {
    const response = await fetch(`${BASE_URL}/tournament/`, {
      method: "GET",
    });
    if (!response.ok) {
      throw new Error("Network response was not ok");
    }
    return await response.json();
  } catch (error) {
    console.error("Error fetching tournament data:", error);
    throw error;
  }
}

export async function addTournamentData(payload) {
  try {
    const response = await fetch(`${BASE_URL}/tournament/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });
    if (!response.ok) {
      throw new Error("Network response was not ok");
    }
    return await response.json();
  } catch (error) {
    console.error("Error adding tournament data:", error);
    throw error;
  }
}

export async function fetchTournamentInfo(tournamentId) {
  try {
    const response = await fetch(`${BASE_URL}/tournament/${tournamentId}`, {
      method: "GET",
    });
    if (!response.ok) {
      throw new Error("Network response was not ok");
    }
    return await response.json();
  } catch (error) {
    console.error("Error fetching tournament info:", error);
    throw error;
  }
}

export async function joinTournament(tournamentId, userId) {
  try {
    const response = await fetch(
      `${BASE_URL}/tournamentParticipants/joinTournament`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ tournament_id: tournamentId, user_id: userId }),
      }
    );
    if (!response.ok) {
      throw new Error("Network response was not ok");
    }
    return await response.json();
  } catch (error) {
    console.error("Error joining tournament:", error);
    throw error;
  }
}

export async function leaveTournament(tournamentId, userId) {
  try {
    const response = await fetch(
      `${BASE_URL}/tournamentParticipants/leaveTournament/${tournamentId}/user/${userId}`,
      {
        method: "DELETE",
      }
    );
    if (!response.ok) {
      throw new Error("Network response was not ok");
    }
    return await response.json();
  } catch (error) {
    console.error("Error leaving tournament:", error);
    throw error;
  }
}

export async function createMatchMakingTournament(tournamentId, roundId) {
  try {
    const response = await fetch(
      `${BASE_URL}/tournamentPairings/createMatchMaking/${tournamentId}/roundId/${roundId}`,
      {
        method: "GET",
      }
    );
    if (!response.ok) {
      throw new Error("Network response was not ok");
    }
    return await response.json();
  } catch (error) {
    console.error("Error creating matchmaking tournament:", error);
    throw error;
  }
}

export async function createMatchMaking(tournamentId, roundId) {
  try {
    const response = await fetch(
      `${BASE_URL}/tournamentPairings/createMatchMaking/${tournamentId}/roundId/${roundId}`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          tournament_id: tournamentId,
          round_id: roundId,
        }),
      }
    );
    if (!response.ok) {
      throw new Error("Network response was not ok");
    }
    return await response.json();
  } catch (error) {
    console.error("Error creating matchmaking:", error);
    throw error;
  }
}
