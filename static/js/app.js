function pingBackend() {
    fetch('/api/health/')
        .then(res => res.json())
        .then(data => alert(data.message));
}
