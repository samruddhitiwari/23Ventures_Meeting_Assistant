document.getElementById("startRecording").addEventListener("click", () => {
    fetch("/record", { method: "POST" })
        .then(response => response.text())
        .then(data => alert(data));
});

document.getElementById("stopRecording").addEventListener("click", () => {
    fetch("/stop", { method: "POST" })
        .then(response => response.text())
        .then(data => alert(data));
});

document.getElementById("summarizeBtn").addEventListener("click", () => {
    const fileInput = document.getElementById("fileInput").files[0];
    if (!fileInput) {
        alert("Please select a file.");
        return;
    }
    
    const formData = new FormData();
    formData.append("file", fileInput);

    fetch("/summarize", {
        method: "POST",
        body: formData
    })
    .then(response => response.text())
    .then(data => document.getElementById("summaryOutput").innerText = data);
});

document.getElementById("searchBtn").addEventListener("click", () => {
    const query = document.getElementById("searchQuery").value;
    fetch(`/search?query=${query}`)
        .then(response => response.json())
        .then(results => {
            const output = results.map(r => `<p><strong>${r.date}:</strong> ${r.content}</p>`).join("");
            document.getElementById("searchResults").innerHTML = output;
        });
});
