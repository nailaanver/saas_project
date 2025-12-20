const token = localStorage.getItem("access");

if (!token) window.location.href = "/login/";

fetch("/api/collaboration/channels/", {
    headers: {
        "Authorization": "Bearer " + token,
        "X-Tenant-ID": TENANT_ID
    }
})
.then(res => res.json())
.then(data => {
    const ul = document.getElementById("channels");
    data.forEach(ch => {
        const li = document.createElement("li");
        li.innerText = "#" + ch.name;
        li.onclick = () => loadMessages(ch.id, ch.name);
        ul.appendChild(li);
    });
});
