// === DOM ===
const skillInput = document.getElementById("skillInput");
const dropdown = document.getElementById("skillsDropdown");
const selectedContainer = document.getElementById("selectedSkills");
const skillsField = document.getElementById("skillsField");

// === STATE ===
let selectedSkills = [];

// === FUNCTIONS (GLOBAL) ===
function openDropdown() {
    dropdown.classList.add("show");
}

function closeDropdown() {
    dropdown.classList.remove("show");
    dropdown.innerHTML = "";
}

function removeSkill(id, chip) {
    selectedSkills = selectedSkills.filter(s => s !== id);
    chip.remove();
    syncHiddenField();
}

function internalAddSkill(skill, silent = false) {
    if (selectedSkills.includes(skill.id)) return;

    selectedSkills.push(skill.id);

    const chip = document.createElement("div");
    chip.className = "skill-chip";
    chip.dataset.id = skill.id;

    chip.innerHTML = `
        <span>${skill.name}</span>
        <img src="/static/assets/icons/Cross.svg">
    `;

    chip.addEventListener("click", () => {
        removeSkill(skill.id, chip);
    });

    selectedContainer.appendChild(chip);

    if (!silent) closeDropdown();
    syncHiddenField();
}

function syncHiddenField() {
    skillsField.value = JSON.stringify(selectedSkills);
}

// === INPUT ===
skillInput.addEventListener("input", async () => {
    const value = skillInput.value.trim();
    if (!value) return closeDropdown();

    const res = await fetch(`/api/skills/?q=${value}`);
    const skills = await res.json();

    dropdown.innerHTML = "";

    skills.forEach(skill => {
        if (selectedSkills.includes(skill.id)) return;

        const li = document.createElement("li");
        li.textContent = skill.name;
        li.addEventListener("click", () => {
            internalAddSkill(skill);
            skillInput.value = "";
        });

        dropdown.appendChild(li);
    });

    dropdown.children.length ? openDropdown() : closeDropdown();
});

// === OUTSIDE CLICK ===
document.addEventListener("click", e => {
    if (!e.target.closest(".skills-step")) closeDropdown();
});

// === INIT EXISTING SKILLS ===
document.addEventListener("DOMContentLoaded", () => {
    if (!window.INITIAL_SKILLS) return;
    INITIAL_SKILLS.forEach(skill => internalAddSkill(skill, true));
});
