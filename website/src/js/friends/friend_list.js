// https://developer.mozilla.org/fr/docs/Web/API/WebSocket

let g_currentFriendList = [];
let errorRetrievingFriends = false;
let g_friendListWebSocket;

// Create WebSocket connection if user was already logged-in when opening the page
function loadFriendsWebsocket()
{
    if (g_friendListWebSocket)
        return;
    let user_token = getCookie("session_token");
    if (user_token && user_token.length > 0) {
        createWebSocketFriendList();
    }
}

function createWebSocketFriendList() {
    let user_token = getCookie("session_token");
    const WEBSOCKET_FRIENDS_URL = `wss://${g_host}:7000/ws/friends/${user_token}/`;
    g_friendListWebSocket = new WebSocket(WEBSOCKET_FRIENDS_URL);

    g_friendListWebSocket.onopen = function (e) {
    }

    g_friendListWebSocket.onclose = function (e) {
    }

    g_friendListWebSocket.onmessage = function (e) {
        try {
            const data = JSON.parse(e.data);
            errorRetrievingFriends = false;
            if (data.friends) {
                g_currentFriendList = data.friends;
                displayCurrentFriendList();
            }
            else if (data.type)
            {
                if (data.type === "new_follower_notification")
                {
                    sendNewFollowerNotification(data.follower_username);
                }
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
    if (errorRetrievingFriends === true) {
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
        let friendElement = document.createElement("li");
        friendElement.id = `user-${friend.user_id}`;
        // friendElement.className = 'list-group-item card-content-background'
        let usernameSpan = document.createElement("span");
        usernameSpan.textContent = friend.username;
        usernameSpan.style.cursor = "pointer";
        usernameSpan.style.textDecoration = "underline";
        
        usernameSpan.addEventListener("click", () => {
            navigate(`/users/profile/${encodeURIComponent(friend.username)}`);
        });
        friendElement.appendChild(usernameSpan);
        
        friendListElement.appendChild(friendElement);        
    })
}

function displayEmptyFriendList() {
    displayMessageInFriendList("...");
}

function displayErrorFriendList() {
    displayMessageInFriendList("Error retriving friends.");
}

function displayMessageInFriendList(message) {
    let friendListElement = document.getElementById('friend-list');
    friendListElement.innerHTML = '';
    let errorElement = document.createElement('li');
    // errorElement.className = 'list-group-item card-content-background';
    errorElement.innerText = message;
    friendListElement.appendChild(errorElement);
}

async function sendNewFollowerNotification(followerUsername)
{
    let key = "new_follower_notification";
    let text = await fetchTranslation(key);

    showNotification(`${text} ${followerUsername}`, 5);
}