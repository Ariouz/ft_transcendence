async function isUserFollowing(user_id, target_id)
{
    let url = `${USERS_SERVICE_URL}/user/friends/follows/${user_id}/${target_id}/`;
    let follows = await fetch(url)
    .then(data => data.json())
    .then(data => { return data.is_following; })
    .catch(error => { console.error(error); return false;});
    return follows;
}

async function followUser(user_id, target_id)
{
    let url = `${USERS_SERVICE_URL}/user/friends/${user_id}/add/${target_id}/`;
    let result = await fetch(url, {
        method: 'POST'
    })
    .then(data => data.json())
    .then(data => { return data; })
    .catch(error => { return error; });
    return result;
}

async function unfollowUser(user_id, target_id)
{
    let url = `${USERS_SERVICE_URL}/user/friends/${user_id}/remove/${target_id}/`;
    let result = await fetch(url, {
        method: 'DELETE'
    })
    .then(data => data.json())
    .then(data => { return data; })
    .catch(error => { return error; });
    return result;
}