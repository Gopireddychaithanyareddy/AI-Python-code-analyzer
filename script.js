document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("runButton").addEventListener("click", () => sendCode("run"));
    document.getElementById("debugButton").addEventListener("click", () => sendCode("debug"));
    document.getElementById("optimizeButton").addEventListener("click", () => sendCode("optimize"));
});

function sendCode(action) {
    let codeInput = document.getElementById("codeInput").value;
    let output = document.getElementById("output");

    if (codeInput.trim() === "") {
        alert("❌ Please enter Python code.");
        return;
    }

    output.value = `⏳ Processing ${action} request... Please wait.`;

    fetch(`http://127.0.0.1:8000/${action}/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ code: codeInput })
    })
    .then(response => response.json())
    .then(data => {
        output.value = data.result || "⚠️ Error processing code.";
    })
    .catch(error => {
        output.value = "❌ Error: Could not connect to server.";
        console.error(error);
    });
}
