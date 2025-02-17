
async function handleGameEvent(data)
{
    if (data.event_type == "malus_ball_flicker") 
    {
        if (window.setFlickerMalus)
        {
            setFlickerMalus(data.event_data);
            await displayEventMessage(data.event_type, `${data.event_data}s`);
        }
    }
    else if (data.event_type == "ball_speed")
    {
        ballSpeed = data.event_data;
        await displayEventMessage(data.event_type, `${ballSpeed > 0 ? "+" : ""}${Math.floor(ballSpeed*100)}%`);
    }
}

async function displayEventMessage(event_type, event_detail)
{
    let eventTranslation = await fetchTranslation(`pong_event_${event_type}`);
    pong_text_overlay.innerText = ` ${eventTranslation} ${event_detail}`;
    pong_text_overlay.classList.add("pong_text_overlay_shown");

    setTimeout(async () => {
        pong_text_overlay.innerText = ``;
        pong_text_overlay.classList.remove("pong_text_overlay_shown");          
    }, 3000);
}

