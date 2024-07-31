// https://developer.mozilla.org/fr/docs/Web/API/WebSocket

let g_currentFriendList = [];
let errorRetrievingFriends = false;
let g_friendListWebSocket;

// Create WebSocket connection if user was already logged-in when opening the page
window.onload = (event) => {
    if (g_friendListWebSocket)
        return;
    let user_token = getCookie("session_token");
    if (user_token && user_token.length > 0) {
        createWebSocketFriendList();
    }
}

function createWebSocketFriendList() {
    let user_token = getCookie("session_token");
    const WEBSOCKET_FRIENDS_URL = `ws://localhost:7000/ws/friends/${user_token}/`;
    g_friendListWebSocket = new WebSocket(WEBSOCKET_FRIENDS_URL);
    console.log("WS: Created WebSocket for user's friend list.");

    g_friendListWebSocket.onopen = function (e) {
        console.log("WS: Opened websocket connection.");
    }

    g_friendListWebSocket.onclose = function (e) {
        console.log("WS: Closed websocket connection.");
    }

    g_friendListWebSocket.onmessage = function (e) {
        console.log("WS: Message received:", e);
        try {
            const data = JSON.parse(e.data);
            errorRetrievingFriends = false;
            if (data.friends) {
                g_currentFriendList = data.friends;
                displayCurrentFriendList();
            }
            else
                errorRetrievingFriends = true;
        } catch (error) {
            errorRetrievingFriends = true;
        }
    };
}

function displayCurrentFriendList() {
    let friendListElement = document.getElementById('friend-list');
    if (friendListElement === null)
        return;
    if (errorRetrievingFriends == true) {
        displayErrorFriendList();
    }
    else if (g_currentFriendList.length > 0) {
        displayFriendList();
    }
    else {
        displayEmptyFriendList();
    }
}

function displayFriendList() {
    let friendListElement = document.getElementById('friend-list');
    friendListElement.innerHTML = '';
    g_currentFriendList.forEach(friend => {
        let friendElement = document.createElement('li');
        friendElement.id = `user-${friend.user_id}`;
        friendElement.className = 'list-group-item card-content-background';
        friendElement.innerText = `${friend.username}`;
        friendListElement.appendChild(friendElement);
    })
}

function displayEmptyFriendList() {
    displayMessageInFriendList("You don't have any friends yet.");
}

function displayErrorFriendList() {
    displayMessageInFriendList("Error retriving friends.");
}

function displayMessageInFriendList(message) {
    let friendListElement = document.getElementById('friend-list');
    friendListElement.innerHTML = '';
    let errorElement = document.createElement('li');
    errorElement.className = 'list-group-item card-content-background';
    errorElement.innerText = message;
    friendListElement.appendChild(errorElement);
}
