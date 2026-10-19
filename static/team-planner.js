const addPlayerButton = document.getElementById("addPlayerButton");
const addPlayerModal = document.getElementById("addPlayerModal");
const closeAddPlayerModal = document.getElementById("closeAddPlayerModal");
const availableProfilesList = document.getElementById("availableProfilesList");
const playerGrid = document.getElementById("playerGrid");

function openAddPlayerModal() {
    addPlayerModal.setAttribute("aria-hidden", "false");
    addPlayerModal.classList.add("active");
}

function closePlayerModal() {
    addPlayerModal.setAttribute("aria-hidden", "true");
    addPlayerModal.classList.remove("active");
}

addPlayerButton.addEventListener("click", openAddPlayerModal);
closeAddPlayerModal.addEventListener("click", closePlayerModal);

addPlayerModal.querySelector(".modal-backdrop")
    .addEventListener("click", closePlayerModal);

availableProfilesList.addEventListener("click", function (event) {
    const profileButton = event.target.closest(".available-profile-option");

    if (!profileButton) {
        return;
    }

    const username = profileButton.dataset.username.trim();

    if (!username) {
        return;
    }

    const alreadyAdded = [...playerGrid.querySelectorAll(".player-name")]
        .some(input => input.value.trim() === username);

    if (alreadyAdded) {
        alert("That player is already in the roster.");
        return;
    }

    const roles = profileButton.dataset.roles || "";
    const heroes = profileButton.dataset.heroes || "";

    const card = document.createElement("article");
    card.className = "player-card";

    const header = document.createElement("div");
    header.className = "player-card-header";

    const avatar = document.createElement("div");
    avatar.className = "player-avatar";
    avatar.textContent = username.slice(0, 2).toUpperCase();

    const identity = document.createElement("div");
    identity.className = "player-identity";

    const nameInput = document.createElement("input");
    nameInput.type = "text";
    nameInput.className = "player-name";
    nameInput.placeholder = "Player name";
    nameInput.value = username;

    const status = document.createElement("span");
    status.className = "player-status";
    status.textContent = "ACTIVE";

    const removeButton = document.createElement("button");
    removeButton.className = "icon-button remove-player";
    removeButton.type = "button";
    removeButton.setAttribute("aria-label", "Remove player");
    removeButton.textContent = "×";

    identity.append(nameInput, status);
    header.append(avatar, identity, removeButton);

    function addPlayerField(labelText, contentElement) {
        const field = document.createElement("div");
        field.className = "player-field";

        const label = document.createElement("label");
        label.textContent = labelText;

        field.append(label, contentElement);
        card.append(field);
    }

    const heroInput = document.createElement("input");
    heroInput.type = "text";
    heroInput.placeholder = "Main character...";
    heroInput.value = heroes.split(",")[0]?.trim() || "";

    const rolesText = document.createElement("span");
    rolesText.className = "selected-roles";
    rolesText.textContent = roles || "No roles listed";

    const rolesDisplay = document.createElement("div");
    rolesDisplay.className = "role-selector";
    rolesDisplay.append(rolesText);

    const strengthsInput = document.createElement("input");
    strengthsInput.type = "text";
    strengthsInput.placeholder = "Player strengths...";

    const weaknessesInput = document.createElement("textarea");
    weaknessesInput.rows = 2;
    weaknessesInput.placeholder = "Player weaknesses...";

    const notesInput = document.createElement("textarea");
    notesInput.rows = 3;
    notesInput.placeholder = "Additional notes...";

    card.append(header);
    addPlayerField("Main / Hero", heroInput);
    addPlayerField("Roles", rolesDisplay);
    addPlayerField("Strengths", strengthsInput);
    addPlayerField("Weaknesses", weaknessesInput);
    addPlayerField("Coach / Team Notes", notesInput);

    playerGrid.append(card);
    closePlayerModal();
});

const lineupHeroes = [
    "Spider-Man",
    "Magik",
    "Star-Lord",
    "Mantis",
    "Iron-Man",
    "Thor",
    "Hulk",
    "Luna Snow",
    "Moon Knight",
    "Psylocke",
    "Scarlet Witch",
    "Venom",
    "Wolverine",
    "Adam",
    "Punisher",
    "Invisible Woman",
    "Human Torch",
    "Jeff TLS",
    "Gorr",
    "Black Panther",
    "Phoenix",
    "Emma Snow",
    "Angela",
    "Blade",
    "CloaknDagger",
    "DareDevil",
    "Steve Rogers",
    "Hawkeye",
    "Loki",
    "Magneto",
    "Squirrel Girl",
    "Ultron",
    "Reed Richards",
    "The Thing",
    "Jubilee",
    "Hood",
    "Rogue",
    "Black Cat",
    "Elsa Bloodstone",
    "Winter Soldier",
    "Black Widow",
    "White Fox",
    "Peni",
    "Cyclops",
    "Iron Fist",
    "Gambit",
    "Groot",
    "Strange",
    "Storm",
    "Rocket",
    "Namor",
    "Deadpool",
    "Hela",
    "Devil Dino"
];

const lineupSlots = document.querySelectorAll(".lineup-slot");

function setupLineup() {
    lineupSlots.forEach((slot) => {
        const heroSelect = slot.querySelector(".slot-hero");

        lineupHeroes.forEach((hero) => {
            const option = document.createElement("option");
            option.value = hero;
            option.textContent = hero;
            heroSelect.appendChild(option);
        });

        slot.querySelector(".slot-hero")
            .addEventListener("change", updateLineupCounts);

        slot.querySelector(".slot-role")
            .addEventListener("change", updateLineupCounts);
    });

    updateLineupCounts();
}

function updateLineupCounts() {
    let filledSlots = 0;
    let vanguards = 0;
    let duelists = 0;
    let strategists = 0;

    lineupSlots.forEach((slot) => {
        const hero = slot.querySelector(".slot-hero").value;
        const role = slot.querySelector(".slot-role").value;

        if (hero && role) {
            filledSlots++;

            if (role === "Vanguard") {
                vanguards++;
            } else if (role === "Duelist") {
                duelists++;
            } else if (role === "Strategist") {
                strategists++;
            }
        }
    });

    document.getElementById("lineupCount").textContent =
        `${filledSlots} / 6`;

    document.getElementById("vanguardCount").textContent = vanguards;
    document.getElementById("duelistCount").textContent = duelists;
    document.getElementById("strategistCount").textContent = strategists;
}

setupLineup();

playerGrid.addEventListener("click", function (event) {
    const removeButton = event.target.closest(".remove-player");

    if (removeButton) {
        removeButton.closest(".player-card").remove();
    }
});

const addScheduleButton = document.getElementById("addScheduleButton");
const scheduleModal = document.getElementById("scheduleModal");
const closeScheduleModal = document.getElementById("closeScheduleModal");

function openScheduleModal() {
    scheduleModal.classList.add("active");
    scheduleModal.setAttribute("aria-hidden", "false");
}

function closeScheduleModalWindow() {
    scheduleModal.classList.remove("active");
    scheduleModal.setAttribute("aria-hidden", "true");
}

if (addScheduleButton && scheduleModal && closeScheduleModal) {
    addScheduleButton.addEventListener("click", openScheduleModal);

    closeScheduleModal.addEventListener(
        "click",
        closeScheduleModalWindow
    );

    const scheduleBackdrop = scheduleModal.querySelector(".modal-backdrop");

    if (scheduleBackdrop) {
        scheduleBackdrop.addEventListener(
            "click",
            closeScheduleModalWindow
        );
    }
} else {
    console.error("Could not find the schedule modal elements.");
}

const saveScheduleButton = document.getElementById("saveScheduleEvent");

if (saveScheduleButton) {
    saveScheduleButton.addEventListener("click", async function () {
        const name = document.getElementById("eventName").value.trim();
        const eventType = document.getElementById("eventType").value;
        const eventDate = document.getElementById("eventDate").value;
        const eventTime = document.getElementById("eventTime").value;
        const timezone = document.getElementById("eventTimezone").value;
        const hours = Number(
            document.getElementById("eventDurationHours").value || 0
        );
        const minutes = Number(
            document.getElementById("eventDurationMinutes").value || 0
        );
        const notes = document.getElementById("eventNotes").value.trim();

        if (!name || !eventDate || !eventTime) {
            alert("Please enter an event name, date, and time.");
            return;
        }

        const eventData = {
            name: name,
            event_type: eventType,
            event_date: eventDate,
            event_time: eventTime,
            timezone: timezone,
            duration_minutes: hours * 60 + minutes,
            notes: notes
        };

        saveScheduleButton.disabled = true;

        try {
            const response = await fetch("/api/schedule", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(eventData)
            });

            const result = await response.json();

            if (!response.ok) {
                throw new Error(result.error || "Could not save the event.");
            }

            alert("Event added to the schedule!");

            const modal = document.getElementById("scheduleModal");
            modal.classList.remove("active");
            modal.setAttribute("aria-hidden", "true");
            await loadScheduleEvents();

        document.getElementById("scheduleModal")
            .querySelector("form")?.reset();

        } catch (error) {
            console.error("Schedule save error:", error);
            alert("Couldn't save the event: " + error.message);
        } finally {
            saveScheduleButton.disabled = false;
        }
    });
}

async function loadScheduleEvents() {
    const scheduleList = document.getElementById("scheduleList");

    if (!scheduleList) return;

    let savedEventsContainer = document.getElementById("savedScheduleEvents");

    if (!savedEventsContainer) {
        savedEventsContainer = document.createElement("div");
        savedEventsContainer.id = "savedScheduleEvents";
        scheduleList.appendChild(savedEventsContainer);
    }

    try {
        const response = await fetch("/api/schedule");
        if (!response.ok) throw new Error("Failed to load events.");

        const data = await response.json();
        const events = Array.isArray(data)
            ? data
            : (data.events || data.schedule || []);

        savedEventsContainer.replaceChildren();

        events.forEach(event => {
            const card = document.createElement("article");
            card.className = "schedule-item";

            const details = document.createElement("div");
            details.className = "schedule-details";

            const title = document.createElement("h3");
            title.textContent = event.name;

            const dateTime = document.createElement("p");
            dateTime.textContent =
                `${event.event_date} · ${event.event_time} (${event.timezone})`;

            const type = document.createElement("p");
            type.textContent = event.event_type;

            details.append(title, dateTime, type);

            if (event.duration_minutes) {
                const duration = document.createElement("p");
                const hours = Math.floor(event.duration_minutes / 60);
                const minutes = event.duration_minutes % 60;

                duration.textContent =
                    `Duration: ${hours > 0 ? hours + " hr " : ""}` +
                    `${minutes > 0 ? minutes + " min" : ""}`.trim();

                details.appendChild(duration);
            }

            if (event.notes) {
                const notes = document.createElement("p");
                notes.textContent = event.notes;
                details.appendChild(notes);
            }

            card.appendChild(details);
            savedEventsContainer.appendChild(card);
        });

    } catch (error) {
        console.error("Error loading schedule:", error);
    }
}
loadScheduleEvents();