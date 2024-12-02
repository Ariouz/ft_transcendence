function stopInterval()
{
    if (g_pongGameInterval)
    {
        pong_text_overlay.classList.remove("pong_text_overlay_shown");
        pong_text_overlay.innerText = "";
        clearInterval(g_pongGameInterval);
        g_pongGameInterval = null;
    }
}

function setScore(game_data)
{
    pong_self_score = document.getElementById("pong_self_score");
    pong_opponent_score = document.getElementById("pong_opponent_score");

    player1_score = game_data.players.player1.score;
    player2_score = game_data.players.player2.score;

    if (g_pongGamePlayerPaddle == 'player1' || g_pongGamePlayerPaddle == 'both')
    {
        pong_self_score.innerText = player1_score;
        pong_opponent_score.innerText = player2_score;
    }
    else
    {
        pong_self_score.innerText = player2_score;
        pong_opponent_score.innerText = player1_score;
    }
}

function updateScore(game_data, data)
{
    setScore(game_data);

    if (g_pongGameOpponentDisconnected) return ;

    countdown_timer = data.countdown_timer;
    scorer = data.scoring_player;

    txt_time = countdown_timer - 3 - 1;
    pong_text_overlay.innerText = getDisplayNameByPlayer(scorer, game_data.players, g_pongUserId) + " scored!";
    pong_text_overlay.classList.add("pong_text_overlay_shown");

    countdown_timer = 4;
    g_pongGameInterval = setInterval(() => {
        if (countdown_timer <= 0 || g_pongGameOpponentDisconnected)
        {
            pong_text_overlay.classList.remove("pong_text_overlay_shown");
            pong_text_overlay.innerText = "";
            stopInterval();
            return ;
        }

        if (txt_time <= 0)
            pong_text_overlay.innerText = countdown_timer;

        if (!pong_text_overlay.classList.contains("pong_text_overlay_shown"))
            pong_text_overlay.classList.add("pong_text_overlay_shown");
        
        txt_time--;
        countdown_timer--;
    }, 1000);
}

function startTimer(countdown_timer)
{
    if (g_pongGameOpponentDisconnected) return ;

    txt_time = countdown_timer - 3 - 1;
    pong_text_overlay.innerText = "Starting in...";
    pong_text_overlay.classList.add("pong_text_overlay_shown");

    countdown_timer = 4;
    g_pongGameInterval = setInterval(() => {
        if (countdown_timer <= 0 || g_pongGameOpponentDisconnected)
        {
            pong_text_overlay.classList.remove("pong_text_overlay_shown");
            pong_text_overlay.innerText = "";
            stopInterval();
            return ;
        }

        if (txt_time <= 0)
            pong_text_overlay.innerText = countdown_timer;

        if (!pong_text_overlay.classList.contains("pong_text_overlay_shown"))
            pong_text_overlay.classList.add("pong_text_overlay_shown");

        txt_time--;
        countdown_timer--;
    }, 1000);
}

function winnerTimer(countdown_timer, winner, game_data)
{
    setScore(game_data);
    pong_text_overlay.innerText = winner + " won the game!";
    pong_text_overlay.classList.add("pong_text_overlay_shown");

    g_pongGameInterval = setInterval(() => {
        if (countdown_timer <= 0)
        {
            pong_text_overlay.classList.remove("pong_text_overlay_shown");
            pong_text_overlay.innerText = "";
            stopInterval();

            g_pongGameWebSocket.close();
            g_pongGameState = null;
            g_pongGamePlayerPaddle = null;
            g_pongGameType = null;
            g_pongGameOpponentDisconnected = false;
            g_pongGameInterval = null;
            
            showMainNavigation();
            showFooter();
            navigate("/pong");
            return ;
        }

        if (!pong_text_overlay.classList.contains("pong_text_overlay_shown"))
            pong_text_overlay.classList.add("pong_text_overlay_shown");
        pong_text_overlay.innerText = winner + " won the game!";

        countdown_timer--;
    }, 1000);
}

function pauseTimer(countdown_timer, player, game_data)
{
    if (!g_pongGameOpponentDisconnected) return ;

    pong_text_overlay.innerText = player + " disconnected - " + countdown_timer;
    pong_text_overlay.classList.add("pong_text_overlay_shown");

    countdown_timer--;
    g_pongGameInterval = setInterval(() => {
        if (countdown_timer <= 0 || !g_pongGameOpponentDisconnected)
        {
            pong_text_overlay.classList.remove("pong_text_overlay_shown");
            pong_text_overlay.innerText = "";
            stopInterval();
            return ;
        }

        if (!pong_text_overlay.classList.contains("pong_text_overlay_shown"))
            pong_text_overlay.classList.add("pong_text_overlay_shown");
            
        pong_text_overlay.innerText = player + " disconnected - " + countdown_timer;
        countdown_timer--;
    }, 1000);
}

function resumeTimer(countdown_timer, player, game_data)
{
    txt_time = countdown_timer - 3 - 1;
    pong_text_overlay.innerText = player + " reconnected";
    pong_text_overlay.classList.add("pong_text_overlay_shown");

    countdown_timer = 4;
    g_pongGameInterval = setInterval(() => {
        if (countdown_timer <= 0)
        {
            pong_text_overlay.classList.remove("pong_text_overlay_shown");
            pong_text_overlay.innerText = "";
            stopInterval();
            return;
        }

        if (!pong_text_overlay.classList.contains("pong_text_overlay_shown"))
            pong_text_overlay.classList.add("pong_text_overlay_shown");

        pong_text_overlay.innerText = txt_time > 0 ? player + " reconnected" : countdown_timer;

        txt_time--;
        countdown_timer--;
    }, 1000);
}