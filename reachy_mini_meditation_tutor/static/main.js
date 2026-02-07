let antennasEnabled = true;
let sessionMinutes = 3;
let breathSoundEnabled = false;

async function updateAntennasState(enabled) {
    try {
        const resp = await fetch("/antennas", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ enabled }),
        });
        const data = await resp.json();
        antennasEnabled = data.antennas_enabled;
        updateUI();
    } catch (e) {
        document.getElementById("status").textContent = "Backend error";
    }
}

async function updateBreathSound(enabled) {
    try {
        const resp = await fetch("/breath_sound", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ enabled }),
        });
        const data = await resp.json();
        breathSoundEnabled = data.breath_sound_enabled;
        updateUI();
    } catch (e) {
        document.getElementById("status").textContent = "Backend error";
    }
}


async function updateSession(minutes) {
    try {
        const resp = await fetch("/session", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ minutes }),
        });
        const data = await resp.json();
        if (!data.ok) {
            document.getElementById("status").textContent = data.error || "Invalid session";
            return;
        }
        sessionMinutes = data.minutes;
        updateUI();
    } catch (e) {
        document.getElementById("status").textContent = "Backend error";
    }
}

async function startSession() {
    try {
        await fetch("/start", { method: "POST" });
        document.getElementById("status").textContent = `Running: ${sessionMinutes} min (inhale 5s / exhale 8s)`;
    } catch (e) {
        document.getElementById("status").textContent = "Backend error";
    }
}

async function stopSession() {
    try {
        await fetch("/stop", { method: "POST" });
        document.getElementById("status").textContent = "Stopping session...";
    } catch (e) {
        document.getElementById("status").textContent = "Backend error";
    }
}

function updateUI() {
    const checkbox = document.getElementById("antenna-checkbox");
    const breathCheckbox = document.getElementById("breath-sound-checkbox");
    const status = document.getElementById("status");
    const sessionButtons = document.querySelectorAll(".session-btn");

    checkbox.checked = antennasEnabled;
    breathCheckbox.checked = breathSoundEnabled;

    sessionButtons.forEach((btn) => {
        const minutes = Number(btn.dataset.minutes);
        btn.classList.toggle("active", minutes === sessionMinutes);
    });

    if (status.textContent === "Ready" || status.textContent.startsWith("Antennas")) {
        status.textContent = `Ready — session: ${sessionMinutes} min`;
    }
}

document.getElementById("antenna-checkbox").addEventListener("change", (e) => {
    updateAntennasState(e.target.checked);
});

document.getElementById("breath-sound-checkbox").addEventListener("change", (e) => {
    updateBreathSound(e.target.checked);
});

document.querySelectorAll(".session-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
        updateSession(Number(btn.dataset.minutes));
    });
});

document.getElementById("start-btn").addEventListener("click", () => {
    startSession();
});

document.getElementById("stop-btn").addEventListener("click", () => {
    stopSession();
});

updateUI();