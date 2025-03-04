async function loadAllPublicProfileData(targetUsername)
    {
        let visitorId = await retrieveId(sessionToken);
        let userData = await retrievePublicProfileDataByUsername(targetUsername);

        if (userData.error)
            navigate("/user-error");
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

            await displayUserStats(userData.user_id);

            await setRightStatus("user_online_status_circle", "user_online_status_radar", userData.user_id);

            // Friends
            followUserButton = document.getElementById("public_profile_follow_user");
            unfollowUserButton = document.getElementById("public_profile_unfollow_user");

            let isFollowing = await isUserFollowing(visitorId.user_id, userData.user_id);
            let isSameUser = visitorId.user_id == userData.user_id;

            followUserButton.style.display = isFollowing || isSameUser ? 'none' : 'block';
            unfollowUserButton.style.display = !isFollowing || isSameUser ? 'none' : 'block';

            historyButton = document.getElementById("public_profile_history_button");
            historyButton.setAttribute('onclick', `navigate('/pong/history/${userData.username}')`);

        }
    }

    async function handleFollowButton(targetUsername) {
        let visitorId = await retrieveId(sessionToken);
        let userData = await retrievePublicProfileDataByUsername(targetUsername);

        unfollowUserButton = document.getElementById("public_profile_unfollow_user");

        followUserButton = document.getElementById("public_profile_follow_user");
        followUserButton.addEventListener('click', async function(event) {
            event.preventDefault();
            result = await followUser(visitorId.user_id, userData.user_id);
            followUserButton.style.display ='none';
            unfollowUserButton.style.display = 'block';
        });
    }

    async function handleUnfollowButton(targetUsername) {
        let visitorId = await retrieveId(sessionToken);
        let userData = await retrievePublicProfileDataByUsername(targetUsername);

        followUserButton = document.getElementById("public_profile_follow_user");

        unfollowUserButton = document.getElementById("public_profile_unfollow_user");
        unfollowUserButton.addEventListener('click', async function(event) {
            event.preventDefault();
            result = await unfollowUser(visitorId.user_id, userData.user_id);
            followUserButton.style.display ='block';
            unfollowUserButton.style.display = 'none';
        });
    }

    async function displayUserStats(userId)
    {
        let statsReq = await getPongUserStats(userId);
        if (!statsReq.data) return ;
        let stats = statsReq.data;
        document.getElementById("user_profile_played_games").innerText = stats.played;
        document.getElementById("user_profile_won_games").innerText = stats.wins;
        document.getElementById("user_profile_lost_games").innerText = stats.loses;
        document.getElementById("user_profile_win_ratio").innerText = stats.ratio;
    }