let currentChannelId = null;

// Load Channels

fetch("api/channels/", {
    headers: {
        "Authorization":"Bearer" + localStorage.getItem("access"),
        "X-Tenant-ID":TENANT_ID
    }
})
.then(res => res.json())
.then(data => {
    let sidebar = document.getElementById("sidebar");
    sidebar.innerHTML = "";

    data.forEach(channel => {
        let div = document.createElement("div");
        div.className="channel";
        div.innerText = "#" + channel.name;
        div.onclick = () => loadMessages(channel.id);
        sidebar.appendChild(div);
        
    });
});

function loadMessages(channelId) {
    currentChannelId = channelId;
    fetch(`/api/messages.?channel_id=${channelId}`, {
        headers:{
            "Authorization":"Bearer" + localStorage.getItem("access"),
            "X-Tenant-ID":TENANT_ID
        }
    })
    .then(res => res.json())
    .then(data => {
        let messagesDiv = document.getElementById("messages");
        messagesDiv.innerHTML = "";

        data.forEach(msg => {
            let p = document.createElement("p");
            p.innerHTML = `<b>${msg.user.username}</b>: ${msg.content}`;
            messagesDiv.appendChild(p);
        })
    })
}

function sendMessage() {
    let text = document.getElementById("messageText").value;

    fetch("/api/messages/send/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": "Bearer" + localStorage.getItem("access"),
            "X-Tenant-ID": TENANT_ID
        },
        body: JSON.stringify({
            channel_id: currentChannelId,
            content: text
        })
    })
    .then(res => res.json())
    .then(() => {
        document.getElementById("messageText").value = "";
        loadMessages(currentChannelId);
    });
}


const token = localStorage.getItem("access");

if (!token) {
    window.location.href = "/login"; // your frontend login page later
}

