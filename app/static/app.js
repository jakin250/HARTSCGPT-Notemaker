const promptDataNode = document.getElementById("promptData");
const promptLibrary = promptDataNode ? JSON.parse(promptDataNode.textContent) : [];
const promptLookup = Object.fromEntries(promptLibrary.map((prompt) => [prompt.id, prompt]));

const promptCards = document.querySelectorAll("[data-prompt-card]");
const fileInput = document.getElementById("documents");
const fileSelectionSummary = document.getElementById("fileSelectionSummary");
const form = document.getElementById("draftForm");
const generateButton = document.getElementById("generateButton");
const copyResultButton = document.getElementById("copyResultButton");
const draftResult = document.getElementById("draftResult");
const maxFiles = fileInput ? Number(fileInput.dataset.maxFiles || "0") : 0;

function updatePromptPreview(promptId) {
    const prompt = promptLookup[promptId];

    if (!prompt) {
        return;
    }

    document.getElementById("promptPreviewTitle").textContent = prompt.name;
    document.getElementById("promptPreviewCategory").textContent = prompt.category;
    document.getElementById("promptPreviewDescription").textContent = prompt.description;
    document.getElementById("promptPreviewDeliverable").textContent = prompt.deliverable;
    document.getElementById("promptPreviewGuidance").textContent = prompt.ui_guidance;
    document.getElementById("selectionSummary").textContent = prompt.name;
    document.getElementById("selectionGuidance").textContent = prompt.ui_guidance;

    promptCards.forEach((card) => {
        card.classList.toggle("is-active", card.dataset.promptId === promptId);
    });
}

promptCards.forEach((card) => {
    const radio = card.querySelector('input[type="radio"]');

    card.addEventListener("click", () => {
        radio.checked = true;
        updatePromptPreview(card.dataset.promptId);
    });
});

if (fileInput && fileSelectionSummary) {
    fileInput.addEventListener("change", () => {
        const files = Array.from(fileInput.files || []);

        if (!files.length) {
            fileSelectionSummary.textContent = "No files selected yet.";
            return;
        }

        if (maxFiles && files.length > maxFiles) {
            fileInput.value = "";
            fileSelectionSummary.textContent = `Please select no more than ${maxFiles} documents.`;
            return;
        }

        const names = files.map((file) => file.name);
        fileSelectionSummary.textContent = `${files.length} file(s): ${names.join(", ")}`;
    });
}

if (form && generateButton) {
    form.addEventListener("submit", () => {
        generateButton.disabled = true;
        generateButton.classList.add("is-loading");
        generateButton.textContent = "Drafting...";
    });
}

if (copyResultButton && draftResult) {
    copyResultButton.addEventListener("click", async () => {
        try {
            await navigator.clipboard.writeText(draftResult.textContent);
            copyResultButton.textContent = "Copied";

            window.setTimeout(() => {
                copyResultButton.textContent = "Copy draft";
            }, 1600);
        } catch (error) {
            copyResultButton.textContent = "Copy failed";

            window.setTimeout(() => {
                copyResultButton.textContent = "Copy draft";
            }, 1600);
        }
    });
}

if (document.body.dataset.hasResult === "true") {
    document.getElementById("result")?.scrollIntoView({ behavior: "smooth", block: "start" });
} else if (document.body.dataset.hasErrors === "true") {
    document.getElementById("feedback")?.scrollIntoView({ behavior: "smooth", block: "start" });
}
