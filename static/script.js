// ---------- Handle 7-day plan form ----------

const form = document.getElementById("plan-form");
const resultDiv = document.getElementById("plan-result");

form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const crop = document.getElementById("crop").value;
    const soil = document.getElementById("soil").value;
    const location = document.getElementById("location").value;
    const lastIrrigation = document.getElementById("last_irrigation").value;
    const sensorMode = document.getElementById("sensor_mode").value;
    const stage = document.getElementById("stage").value; // NEW

    const payload = {
        crop,
        soil,
        location,
        last_irrigation: lastIrrigation,
        sensor_mode: sensorMode,
        stage            // sent, even if backend ignores it for now
    };

    try {
        const res = await fetch("/plan", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });

        if (!res.ok) {
            const err = await res.json();
            resultDiv.innerHTML = `<p style="color:red;">${err.error || "Error"}</p>`;
            document.getElementById("kpi-summary").innerHTML = "";
            return;
        }

        const plan = await res.json();
        renderPlan(plan);
    } catch (err) {
        resultDiv.innerHTML = `<p style="color:red;">Failed to fetch plan.</p>`;
        document.getElementById("kpi-summary").innerHTML = "";
        console.error(err);
    }
});

function renderPlan(plan) {
    const kpiDiv = document.getElementById("kpi-summary");

    if (!Array.isArray(plan) || plan.length === 0) {
        resultDiv.innerHTML = "<p>No plan data.</p>";
        kpiDiv.innerHTML = "";
        return;
    }

    let irrigateCount = 0;
    let skipCount = 0;

    let html = `
        <table>
            <thead>
                <tr>
                    <th>Day</th>
                    <th>Date</th>
                    <th>Action</th>
                    <th>Reason</th>
                    <th>Rain chance (%)</th>
                    <th>Soil moisture (%)</th>
                </tr>
            </thead>
            <tbody>
    `;

    plan.forEach(row => {
        if (row.action === "Irrigate once") irrigateCount++;
        if (row.action === "Skip irrigation") skipCount++;

        const moistureText = row.soil_moisture !== null && row.soil_moisture !== undefined
            ? row.soil_moisture
            : "-";

        html += `
            <tr>
                <td>${row.day}</td>
                <td>${row.date}</td>
                <td class="${row.color}">${row.action}</td>
                <td>${row.reason}</td>
                <td>${row.rain_prob}</td>
                <td>${moistureText}</td>
            </tr>
        `;
    });

    html += "</tbody></table>";
    resultDiv.innerHTML = html;

    kpiDiv.innerHTML = `
        <p><strong>Weekly summary:</strong>
        ${irrigateCount} planned irrigation event(s),
        ${skipCount} irrigation(s) avoided due to expected rainfall.</p>
    `;
}


// ---------- Simple Q&A chat ----------

const askBtn = document.getElementById("ask-btn");
const questionInput = document.getElementById("question");
const chatArea = document.getElementById("chat-area");

if (askBtn) {
    askBtn.addEventListener("click", handleAsk);
    questionInput.addEventListener("keypress", (e) => {
        if (e.key === "Enter") {
            e.preventDefault();
            handleAsk();
        }
    });
}

async function handleAsk() {
    const q = questionInput.value.trim();
    if (!q) return;

    addChatBubble("You", q);
    questionInput.value = "";

    try {
        const res = await fetch("/ask", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ question: q })
        });
        const data = await res.json();
        addChatBubble("Coach", data.answer);
    } catch (err) {
        console.error(err);
        addChatBubble("Coach", "Error getting answer. Please try again.");
    }
}

function addChatBubble(sender, text) {
    const div = document.createElement("div");
    div.className = sender === "You" ? "bubble you" : "bubble coach";
    div.textContent = `${sender}: ${text}`;
    chatArea.appendChild(div);
    chatArea.scrollTop = chatArea.scrollHeight;
}
