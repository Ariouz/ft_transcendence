function addFloor(floorId)
{
    container = document.getElementById("users_list_container");
    floor = document.createElement("div");
    floor.classList.add("users_list_floor");
    floor.id = "users_list_floor_"+floorId;
    container.appendChild(floor);
}

function addUserCard(username, avatar, floorId)
{
    container = document.getElementById("users_list_floor_"+floorId);
    if (container == null)
        {
        addFloor(floorId);
        container = document.getElementById("users_list_floor_"+floorId);
    }
    
    element = document.createElement("div");
    element.classList.add("user_list_item");
    
    element.innerHTML = `<div class="user_list_card_top"> \
                                <div class="user_list_card_top_avatar_container"> \
                                    <img src="${avatar}" alt="avatar" \
                                    class="rounded-circle" id="" style="max-width: 180px; height: auto;"> \
                                </div> \
                                <span>${username}</span> \
                            </div> \
                            <div class="user_list_card_bottom"> \
                                <button class="btn btn-outline-primary" onclick="navigate('/users/profile/${username}')">View profile</button> \
                            </div>`;
    container.appendChild(element);
}

async function loadUsers()
{
    userList = await retrieveAllUsers()
    .then(data => {
        users = [];
        for (userId in data)
            {
            userData = data[userId];
            username = userData.username;
            avatar = userData.avatar;
            
            users.push({"id": userId, "username":username, "avatar":avatar});
        }
        return users;
    }).catch(error => { console.error(error) });
    return userList;
}

async function displayCards(userList)
{
    floorId = 0;
    for (user of userList)
        {
        addUserCard(user.username, user.avatar, Math.floor(floorId / 5));
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
    users = await loadUsers();
    displayCards(users);
    
    searchBar = document.getElementById("userlist_search_bar");
    searchBar.addEventListener('input', function (event) {
        searchUsername = event.target.value;
        
        container = document.getElementById("users_list_container");
        container.innerHTML = "";
        
        newusers = searchByUsername(users, searchUsername)
        .then (newusers => {
            displayCards(newusers);
        });
    });
    
};

loadUserLists();