# DocTailor — Intelligent Document Customization Toolkit

DocTailor is a lightweight framework that helps teams create, update, and customize existing document templates for different clients using structured rules, metadata, and (optionally) LLMs.

It is designed for:

- Technical documentation teams
- Consulting & service companies
- Freelancers who need client-specific templates
- Engineers who automate doc generation or updates

## 🚀 Features
- ✏️ **Template-Based Editing** — Maintain master templates and derive client versions easily.
- 🔄 **Smart Update Rules** — Apply consistent formatting, terminology, and branding.
- 🤖 **LLM Integration (Optional)** — Use any LLM (ChatGPT, Claude, local models) to auto-refine content.
- 🏗️ **Pluggable Architecture** — Add new processors (e.g., latex, docx, pdf).
- 🗂️ **Versioned Template Management** — Track changes across multiple client documents.
- ⚡ **Command-Line Assistant** — Generate docs with a single command.

## 📁 Folder Structure
```
DocTailor/
│
├── templates/          # Base reusable templates
│   └── base.md
│
├── clients/            # Client-specific outputs
│   └── clientA/
│       └── report.md
│
├── rules/              # Custom update rules
│   ├── branding.json
│   └── terminology.json
│
├── engine/             # Core code
│   ├── parser.py
│   ├── updater.py
│   ├── llm_adapter.py
│   └── render.py
│
└── README.md
```

## ⚙️ How It Works
1️⃣ **Start with a base template**
   Write your generic template under `templates/`.

2️⃣ **Define client rules**
   Inside `rules/` set:
   - Branding (colors, logos, product names)
   - Tone preferences (formal, marketing, technical)
   - Terminology replacements
   - Optional metadata (region, industry)

3️⃣ **Generate a client-specific doc**
   ```bash
   python generate.py --template base.md --client clientA
   ```

4️⃣ **(Optional) Use LLM enhancement**
   ```bash
   python generate.py --template base.md --client clientA --llm gpt-5
   ```

## 🧩 Customization Rules Example

**rules/terminology.json:**
```json
{
  "replace": {
    "user": "client",
    "system": "platform",
    "AI model": "intelligence engine"
  }
}
```

**rules/branding.json:**
```json
{
  "company_name": "Acme Corp",
  "color_primary": "#003399",
  "tagline": "Precision Delivered."
}
```

## 🤖 LLM Use Cases
- Rewrite content in client-specific tone
- Add missing sections automatically
- Improve grammar/flow
- Re-structure existing documents
- Generate tailored summaries

LLMs are optional — the engine works fully offline if preferred.

## 🔧 Installation
```bash
git clone https://github.com/<your-username>/DocTailor
cd DocTailor
pip install -r requirements.txt
```

## 🏁 Quick Example
**Input Template (`templates/base.md`):**
```markdown
## Service Overview
Our system provides {service_description}.
```

**Client Rule (in `rules/` or passed via CLI):**
```json
{
  "service_description": "AI-driven analytics for retail optimization"
}
```

**✔️ Output (`clients/clientA/report.md`):**
```markdown
## Service Overview
Our platform provides AI-driven analytics for retail optimization.
```

## 📜 License
MIT License — free for commercial and personal use.

## 🤝 Contributing
Pull requests are welcome!
Open an issue if you need new processors (LaTeX, Word, PDF, etc.)