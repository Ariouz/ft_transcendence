const BASE_URL = "https://localhost:8002";

export async function getLobbyData() {
  try {
    const response = await fetch(`${BASE_URL}lobby/`, {
      method: "GET",
    });
    if (!response.ok) {
      throw new Error(`[${response.status}] Network response was not ok`);
    }
    return await response.json();
  } catch (error) {
    console.error("Error fetching lobby data:", error);
    throw error;
  }
}

export async function addLobbyData(payload) {
  try {
    const response = await fetch(`${BASE_URL}lobby/`, {
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
    console.error("Error adding lobby data:", error);
    throw error;
  }
}

export async function handlePutLobby(payload) {
  try {
    const response = await fetch(
      `${BASE_URL}lobby/${payload?.lobby_id}/userId/${payload?.user_id}`,
      {
        method: "PUT",
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
        },
      }
    );
    if (!response.ok) {
      throw new Error("Network response was not ok");
    }
    return await response.json();
  } catch (error) {
    console.error("Error updating lobby data:", error);
    throw error;
  }
}
