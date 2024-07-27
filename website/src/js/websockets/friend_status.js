let url = `ws://localhost:8001/ws/socket-server/`

const chatSocket = new WebSocket(url)

chatSocket.onmessage = function (e) {
    let data = JSON.parse(e.data)
    console.log("Data:", data)
}
