const skillInput = document.getElementById("skillInput");
const dropdown = document.getElementById("skillsDropdown");
const selectedContainer = document.getElementById("selectedSkills");

let selectedSkills = [];

/* --- загрузка существующих навыков --- */
initialSkills.forEach(skill => addSkill(skill));

/* --- поиск навыков --- */
skillInput.addEventListener("input", async () => {
    const value = skillInput.value.trim();
    if (!value) {
        dropdown.style.display = "none";
        return;
    }

    const res = await fetch(`/api/skills/?q=${value}`);
    const skills = await res.json();

    dropdown.innerHTML = "";

    skills.forEach(skill => {
        if (selectedSkills.includes(skill.id)) return;

        const li = document.createElement("li");
        li.textContent = skill.name;
        li.onclick = () => addSkill(skill);

        dropdown.appendChild(li);
    });

    dropdown.style.display = skills.length ? "block" : "none";
});

/* --- добавление навыка --- */
function addSkill(skill) {
    if (selectedSkills.includes(skill.id)) return;

    selectedSkills.push(skill.id);

    const chip = document.createElement("div");
    chip.className = "skill-chip";
    chip.innerHTML = `
        ${skill.name}
        <img src="/static/assets/icons/Cross.svg" class="skill-remove">
    `;

    chip.querySelector(".skill-remove").onclick = () => {
        selectedSkills = selectedSkills.filter(id => id !== skill.id);
        chip.remove();
    };

    selectedContainer.appendChild(chip);
    dropdown.style.display = "none";
    skillInput.value = "";
}
