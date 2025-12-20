const API_URL = "/api/collaboration/channels/create/";

console.log("create_channel.js loaded");

function createChannel() {
    console.log("Create channel clicked");

    const name = document.getElementById("channelName").value;
    const error = document.getElementById("error");

    error.innerText = "";

    const token = localStorage.getItem("access"); // ✅ MOVE HERE

    if (!token) {
        error.innerText = "You are not logged in.";
        return;
    }

    if (!name) {
        error.innerText = "Channel name required";
        return;
    }

    fetch(API_URL, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + token,
            "X-Tenant-ID": TENANT_ID
        },
        body: JSON.stringify({ name })
    })
    .then(async res => {
        const data = await res.json();
        return { status: res.status, data };
    })
    .then(result => {
        console.log("API result:", result);

        if (result.status !== 201) {
            error.innerText = result.data.error || "Permission denied";
        } else {
            alert("Channel created!");
            window.location.href = `/api/collaboration/workspace/${TENANT_ID}/`;
        }
    })
    .catch(err => {
        console.error(err);
        error.innerText = "Something went wrong";
    });
}
