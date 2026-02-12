// State
let antennasEnabled = true;
let sessionMinutes = 3;
let breathSoundEnabled = false;
let isRunning = false;
let sessionTimer = null;
let breathingTimer = null;

// Constants
const INHALE_SECONDS = 5;
const EXHALE_SECONDS = 8;
const CYCLE_SECONDS = INHALE_SECONDS + EXHALE_SECONDS;

// DOM elements
const breathingCircle = document.getElementById("breathing-circle");
const phaseText = document.getElementById("phase-text");
const timerText = document.getElementById("timer-text");
const startBtn = document.getElementById("start-btn");
const stopBtn = document.getElementById("stop-btn");
const antennaCheckbox = document.getElementById("antenna-checkbox");
const breathSoundCheckbox = document.getElementById("breath-sound-checkbox");
const durationButtons = document.querySelectorAll(".duration-btn");

// API calls
async function updateAntennasState(enabled) {
    try {
        const resp = await fetch("/antennas", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ enabled }),
        });
        const data = await resp.json();
        antennasEnabled = data.antennas_enabled;
        antennaCheckbox.checked = antennasEnabled;
    } catch (e) {
        console.error("Backend error:", e);
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
        breathSoundCheckbox.checked = breathSoundEnabled;
    } catch (e) {
        console.error("Backend error:", e);
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
        if (data.ok) {
            sessionMinutes = data.minutes;
            updateDurationButtons();
        }
    } catch (e) {
        console.error("Backend error:", e);
    }
}

async function startSession() {
    try {
        await fetch("/start", { method: "POST" });
        isRunning = true;
        updateControlsVisibility();
        startBreathingAnimation();
        startCountdown(sessionMinutes * 60);
    } catch (e) {
        console.error("Backend error:", e);
    }
}

async function stopSession() {
    try {
        await fetch("/stop", { method: "POST" });
        endSession();
    } catch (e) {
        console.error("Backend error:", e);
    }
}

// UI updates
function updateDurationButtons() {
    durationButtons.forEach((btn) => {
        const minutes = Number(btn.dataset.minutes);
        btn.classList.toggle("active", minutes === sessionMinutes);
    });
}

function updateControlsVisibility() {
    if (isRunning) {
        startBtn.classList.add("hidden");
        stopBtn.classList.remove("hidden");
        durationButtons.forEach((btn) => (btn.disabled = true));
    } else {
        startBtn.classList.remove("hidden");
        stopBtn.classList.add("hidden");
        durationButtons.forEach((btn) => (btn.disabled = false));
    }
}

function formatTime(seconds) {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, "0")}`;
}

// Breathing animation
function startBreathingAnimation() {
    let cycleTime = 0;

    function updateBreathing() {
        if (!isRunning) return;

        const phase = cycleTime < INHALE_SECONDS ? "inhale" : "exhale";
        const phaseTime = phase === "inhale" ? cycleTime : cycleTime - INHALE_SECONDS;

        // Update text
        phaseText.textContent = phase === "inhale" ? "Inhale" : "Exhale";

        // Update circle class (restart animation)
        breathingCircle.classList.remove("inhale", "exhale");
        if (phaseTime === 0) {
            // Force reflow to restart animation
            void breathingCircle.offsetWidth;
            breathingCircle.classList.add(phase);
        }

        // Advance cycle time
        cycleTime = (cycleTime + 1) % CYCLE_SECONDS;

        breathingTimer = setTimeout(updateBreathing, 1000);
    }

    // Start with inhale
    breathingCircle.classList.add("inhale");
    phaseText.textContent = "Inhale";
    cycleTime = 1;
    breathingTimer = setTimeout(updateBreathing, 1000);
}

function startCountdown(totalSeconds) {
    let remaining = totalSeconds;
    timerText.textContent = formatTime(remaining);

    sessionTimer = setInterval(() => {
        remaining--;
        timerText.textContent = formatTime(remaining);

        if (remaining <= 0) {
            endSession();
        }
    }, 1000);
}

function endSession() {
    isRunning = false;

    // Clear timers
    if (sessionTimer) {
        clearInterval(sessionTimer);
        sessionTimer = null;
    }
    if (breathingTimer) {
        clearTimeout(breathingTimer);
        breathingTimer = null;
    }

    // Reset UI
    breathingCircle.classList.remove("inhale", "exhale");
    phaseText.textContent = "Complete";
    timerText.textContent = "🙏";
    updateControlsVisibility();

    // Reset after a moment
    setTimeout(() => {
        if (!isRunning) {
            phaseText.textContent = "Ready";
            timerText.textContent = "--:--";
        }
    }, 3000);
}

// Event listeners
antennaCheckbox.addEventListener("change", (e) => {
    updateAntennasState(e.target.checked);
});

breathSoundCheckbox.addEventListener("change", (e) => {
    updateBreathSound(e.target.checked);
});

durationButtons.forEach((btn) => {
    btn.addEventListener("click", () => {
        if (!isRunning) {
            updateSession(Number(btn.dataset.minutes));
        }
    });
});

startBtn.addEventListener("click", startSession);
stopBtn.addEventListener("click", stopSession);

// Initialize
updateDurationButtons();
