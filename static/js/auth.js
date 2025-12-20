function login() {
    fetch("/api/token/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            username: document.getElementById("username").value,
            password: document.getElementById("password").value
        })
    })
    .then(res => res.json())
    .then(data => {
        if (data.access) {
            localStorage.setItem("access", data.access);
            localStorage.setItem("refresh", data.refresh);
            window.location.href = "/workspace/";
        } else {
            document.getElementById("error").innerText = "Invalid credentials";
        }
    });
}

function refreshToken() {
    fetch("/api/token/refresh/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            refresh: localStorage.getItem("refresh")
        })
    })
    .then(res => res.json())
    .then(data => {
        if (data.access) {
            localStorage.setItem("access", data.access);
        }
    });
}

setInterval(refreshToken, 4 * 60 * 1000);
