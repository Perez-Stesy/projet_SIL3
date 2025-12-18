const yearInput = document.getElementById("year");
const nameInput = document.getElementById("name");
const codeInput = document.getElementById("code");
const descriptionInput = document.getElementById("description");

const previewYear = document.getElementById("preview-year");
const previewName = document.getElementById("preview-name");
const previewCode = document.getElementById("preview-code");

const btnCurrentYear = document.getElementById("btn-current-year");
const btnGenerateCode = document.getElementById("btn-generate-code");
const liveStatus = document.getElementById("live-status");
const form = document.getElementById("promotion-form");
const submitBtn = document.getElementById("submit-btn");

function safeText(value, fallback) {
    if (typeof value !== "string" || value.trim() === "") return fallback;
    return value.trim();
}

function updatePreview() {
    const yearValue = safeText(yearInput?.value ?? "", "20••");
    const nameValue = safeText(nameInput?.value ?? "", "Nom de la promotion");
    const codeValue = safeText(codeInput?.value ?? "", "CODE-XXX");

    if (previewYear) previewYear.textContent = yearValue;
    if (previewName) previewName.textContent = nameValue;
    if (previewCode) previewCode.textContent = codeValue.toUpperCase();

    if (liveStatus) {
        liveStatus.textContent = "Modifications non enregistrées…";
    }
}

function generateCode() {
    const year = safeText(yearInput?.value ?? "", "");
    const name = safeText(nameInput?.value ?? "", "");

    const yearSuffix = year ? year.slice(-2) : "XX";
    let base = name || "PROMO";

    base = base
        .normalize("NFD")
        .replace(/[\u0300-\u036f]/g, "")
        .toUpperCase()
        .replace(/[^A-Z0-9]+/g, "-")
        .replace(/^-+|-+$/g, "");

    const autoCode = `${base || "PROMO"}-${yearSuffix}`;

    if (codeInput) {
        codeInput.value = autoCode;
        updatePreview();
    }
}

if (yearInput) {
    yearInput.addEventListener("input", updatePreview);
}
if (nameInput) {
    nameInput.addEventListener("input", updatePreview);
}
if (codeInput) {
    codeInput.addEventListener("input", updatePreview);
}
if (descriptionInput) {
    descriptionInput.addEventListener("input", () => {
        if (liveStatus) {
            liveStatus.textContent = "Modifications non enregistrées…";
        }
    });
}

if (btnCurrentYear && yearInput) {
    btnCurrentYear.addEventListener("click", () => {
        const now = new Date();
        yearInput.value = now.getFullYear().toString();
        yearInput.dispatchEvent(new Event("input"));
    });
}

if (btnGenerateCode) {
    btnGenerateCode.addEventListener("click", () => {
        generateCode();
    });
}

if (form && submitBtn && liveStatus) {
    form.addEventListener("submit", () => {
        submitBtn.disabled = true;
        submitBtn.textContent = "Création en cours…";
        liveStatus.textContent = "Envoi du formulaire…";
    });
}

updatePreview();




