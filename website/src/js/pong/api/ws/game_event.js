
async function handleGameEvent(data)
{
    console.log(data);
    if (data.event_type == "malus_ball_flicker") 
    {
        if (window.setFlickerMalus)
            setFlickerMalus(data.event_data);
    }
    
    // else if (data.event_type == "theme") 
    // {
    //     if (window.changeTheme)
    //     {
    //         changeTheme(data.event_data);
    //         if(document.getElementById("pongBackgroundImage"))
    //         {
    //             const imageUrl = getStyle('--canvas-background-url').trim().replace(/^["']|["']$/g, '');
    //             await preloadImage(imageUrl)
    //             requestAnimationFrame(() => setImageBackground(imageUrl));
                
    //         }

    //     }
    // }
}

