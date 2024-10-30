async function loadAllProfileData()
    {
        let visitorId = await retrieveId(sessionToken);
        let userData = await retrievePublicProfileDataByUsername(username);

        if (userData.error)
            navigate("/error");
        else
        {
            document.getElementById("profile_username").innerText = userData.username;
            document.getElementById("profile_user_avatar").src = userData.avatar;
            document.getElementById("profile_user_status_message").innerText = userData.status_message;
            document.getElementById("profile_user_fullname").innerText = userData.full_name;
            document.getElementById("profile_user_displayname").innerText = userData.display_name;
            document.getElementById("profile_user_email").innerText = userData.email;
            document.getElementById("profile_user_lang").innerText = await getLanguageDisplayName(userData.lang);
            document.getElementById("profile_user_intra_link").href = `https://profile.intra.42.fr/users/${userData.username}`;

            githubContainer = document.getElementById("profile_user_github_container");
            githubLink = document.getElementById("profile_user_github_link");

            if (userData.github != "null")
            {
                githubContainer.style.display = 'flex';
                githubContainer.classList.add("d-flex");
            }
            githubLink.href = "https://github.com/" + userData.github;

            await setRightStatus("user_online_status_circle", "user_online_status_radar", userData.user_id);

            // Friends
            followUserButton = document.getElementById("public_profile_follow_user");
            unfollowUserButton = document.getElementById("public_profile_unfollow_user");

            let isFollowing = await isUserFollowing(visitorId.user_id, userData.user_id);
            let isSameUser = visitorId.user_id == userData.user_id;

            followUserButton.style.display = isFollowing || isSameUser ? 'none' : 'block';
            unfollowUserButton.style.display = !isFollowing || isSameUser ? 'none' : 'block';

        }
    }

    async function handleFollowButton() {
        let visitorId = await retrieveId(sessionToken);
        let userData = await retrievePublicProfileDataByUsername(username);

        unfollowUserButton = document.getElementById("public_profile_unfollow_user");

        followUserButton = document.getElementById("public_profile_follow_user");
        followUserButton.addEventListener('click', async function(event) {
            event.preventDefault();
            result = await followUser(visitorId.user_id, userData.user_id);
            followUserButton.style.display ='none';
            unfollowUserButton.style.display = 'block';
        });
    }

    async function handleUnfollowButton() {
        let visitorId = await retrieveId(sessionToken);
        let userData = await retrievePublicProfileDataByUsername(username);

        followUserButton = document.getElementById("public_profile_follow_user");

        unfollowUserButton = document.getElementById("public_profile_unfollow_user");
        unfollowUserButton.addEventListener('click', async function(event) {
            event.preventDefault();
            result = await unfollowUser(visitorId.user_id, userData.user_id);
            followUserButton.style.display ='block';
            unfollowUserButton.style.display = 'none';
        });
    }