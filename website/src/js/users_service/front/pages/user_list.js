function addFloor(floorId)
{
    let container = document.getElementById("users_list_container");
    let floor = document.createElement("div");
    floor.classList.add("users_list_floor");
    floor.id = "users_list_floor_"+floorId;
    container.appendChild(floor);
}

async function addUserCard(username, avatar, floorId, userId)
{
    let container = document.getElementById("users_list_floor_"+floorId);
    if (container == null)
        {
        addFloor(floorId);
        container = document.getElementById("users_list_floor_"+floorId);
    }

    let element = document.createElement("div");
    element.classList.add("user_list_item");
    
    element.innerHTML = `<div class="user_list_card_top"> \
            <div class="user_list_card_top_avatar_container"> \
                <img src="" alt="avatar" \
                    class="rounded-circle" id="" style="max-width: 180px; height: auto;"> \
            </div> \
            <span> \
                <div class="online-status-container"> \
                    <div class="online-status-circle" id="user_online_status_circle-${userId}"></div> \
                    <div class="online-status-radar" id="user_online_status_radar-${userId}"></div> \
                </div> \
                <span class="username"></span> \
            </span> \
        </div> \
        <div class="user_list_card_bottom"> \
            <span class="custom_button custom_button_blue"></span> \
        </div>`;

    element.querySelector("img").src = avatar;
    element.querySelector(".username").textContent = username;
    element.querySelector(".custom_button").textContent = await fetchTranslation("view_profile");
        element.querySelector(".custom_button").addEventListener("click", () => {
        navigate(`/users/profile/${encodeURIComponent(username)}`);
    });

    container.appendChild(element);
    setRightStatus(`user_online_status_circle-${userId}`, `user_online_status_radar-${userId}`, userId);
}

async function loadUsers()
{
    userList = await retrieveAllUsers()
    .then(data => {
        let users = [];
        for (let userId in data)
        {
            let userData = data[userId];
            let username = userData.username;
            let avatar = userData.avatar;

            users.push({"id": userId, "username":username, "avatar":avatar});
        }
        return users;
    }).catch(error => { console.log(error) });
    return userList;
}

async function displayCards(userList)
{
    let floorId = 0;
    for (user of userList)
        {
        await addUserCard(user.username, user.avatar, Math.floor(floorId / 5), user.id);
        floorId++;
    }
}

async function searchByUsername(users, username)
{
    username = username.toLowerCase();
    return users.filter(user => user.username.toLowerCase().startsWith(username));
}

async function loadUserLists()
{
    let users = await loadUsers();
    displayCards(users);

    let searchBar = document.getElementById("userlist_search_bar");
    searchBar.addEventListener('input', function (event) {
        let searchUsername = event.target.value;

        let container = document.getElementById("users_list_container");
        container.innerHTML = "";

        searchByUsername(users, searchUsername)
        .then (newusers => {
            displayCards(newusers);
        }).catch(error => {});
    });
    
}

loadUserLists();