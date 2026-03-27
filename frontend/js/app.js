document.addEventListener('DOMContentLoaded', function() {
    const templateSelect = document.getElementById('templateSelect');
    const clientSelect = document.getElementById('clientSelect');
    const generateBtn = document.getElementById('generateBtn');
    const previewBtn = document.getElementById('previewBtn');
    const downloadBtn = document.getElementById('downloadBtn');
    const copyBtn = document.getElementById('copyBtn');
    const previewArea = document.getElementById('previewArea');
    const llmProviderSelect = document.getElementById('llmProvider');
    const llmModelInput = document.getElementById('llmModel');
    const llmInstructionsTextarea = document.getElementById('llmInstructions');
    const configForm = document.getElementById('configForm');

    let lastGeneratedContent = '';

    // Load templates and clients
    async function loadTemplates() {
        try {
            const response = await fetch('/templates');
            const templates = await response.json();
            templateSelect.innerHTML = '<option value="">Select a template...</option>' +
                templates.map(t => `<option value="${t}">${t}</option>`).join('');
        } catch (error) {
            console.error('Error loading templates:', error);
        }
    }

    async function loadClients() {
        try {
            const response = await fetch('/clients');
            const clients = await response.json();
            clientSelect.innerHTML = '<option value="">Select a client...</option>' +
                clients.map(c => `<option value="${c}">${c}</option>`).join('');
        } catch (error) {
            console.error('Error loading clients:', error);
        }
    }

    // Fetch rules for a client
    async function loadClientRules(clientName) {
        try {
            const response = await fetch(`/rules/${clientName}`);
            if (!response.ok) return {};
            return await response.json();
        } catch (error) {
            console.error('Error loading client rules:', error);
            return {};
        }
    }

    // Update form with client rules
    async function updateFormWithRules(clientName) {
        const rules = await loadClientRules(clientName);
        // For now, we just log the rules; in a more advanced version, we could auto-fill fields
        console.log('Rules for', clientName, ':', rules);
    }

    // Event listeners
    clientSelect.addEventListener('change', function() {
        if (this.value) {
            updateFormWithRules(this.value);
        }
    });

    configForm.addEventListener('submit', function(e) {
        e.preventDefault();
        generateDocument();
    });

    previewBtn.addEventListener('click', function() {
        generateDocument(true);
    });

    downloadBtn.addEventListener('click', function() {
        if (lastGeneratedContent) {
            const blob = new Blob([lastGeneratedContent], { type: 'text/markdown' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `${clientSelect.value || 'document'}.md`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
        }
    });

    copyBtn.addEventListener('click', function() {
        if (lastGeneratedContent) {
            navigator.clipboard.writeText(lastGeneratedContent).then(() => {
                alert('Content copied to clipboard!');
            }).catch(err => {
                console.error('Failed to copy:', err);
                alert('Failed to copy to clipboard');
            });
        }
    });

    // Main function to generate/preview document
    async function generateDocument(previewOnly = false) {
        const template = templateSelect.value;
        const client = clientSelect.value;
        const llmProvider = llmProviderSelect.value || null;
        const llmModel = llmModelInput.value || null;
        const llmInstructions = llmInstructionsTextarea.value;

        if (!template || !client) {
            alert('Please select both a template and a client.');
            return;
        }

        try {
            // Show loading state
            previewArea.innerHTML = '<p>Generating document...</p>';
            generateBtn.disabled = true;
            previewBtn.disabled = true;

            // Prepare request data
            const data = {
                template: template,
                client: client,
                llm: llmProvider,
                llm_model: llmModel,
                llm_instructions: llmInstructions
            };

            const endpoint = previewOnly ? '/preview' : '/generate';
            const response = await fetch(endpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });

            const result = await response.json();

            if (!response.ok) {
                throw new Error(result.error || 'Unknown error');
            }

            if (previewOnly) {
                // Just show preview
                previewArea.innerHTML = `<pre>${result.content}</pre>`;
                lastGeneratedContent = result.content;
                downloadBtn.disabled = false;
            } else {
                // Show success and preview
                previewArea.innerHTML = `<pre>${result.content}</pre>`;
                lastGeneratedContent = result.content;
                downloadBtn.disabled = false;
                alert(result.message || 'Document generated successfully!');
            }
        } catch (error) {
            console.error('Error:', error);
            previewArea.innerHTML = `<p class="error">Error: ${error.message}</p>`;
            alert('Error generating document: ' + error.message);
        } finally {
            generateBtn.disabled = false;
            previewBtn.disabled = false;
        }
    }

    // Initialize
    loadTemplates();
    loadClients();
});