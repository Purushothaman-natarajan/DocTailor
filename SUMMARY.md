DocTailor Project Summary
========================

## Project Structure
- Backend: Flask API server (backend/app.py)
- Frontend: HTML/CSS/JS interface (frontend/)
- Core Engine: Template processing with LLM support (engine/)
- CLI Tool: Command-line document generation (generate.py)
- Templates: Base templates in document_templates/
- Rules: Client-specific configurations in rules/
- Setup Scripts: Windows batch and PowerShell installers

## Key Features
✅ Template-based editing with placeholder replacement
✅ Smart update rules (terminology, branding)
✅ Optional LLM integration (OpenAI, Anthropic, Google)
✅ Pluggable architecture for custom processors
✅ Versioned template management
✅ Command-line interface for automation
✅ Web interface with live preview
✅ GitHub Pages documentation site
✅ Environment variable support for API keys
✅ Cross-platform setup scripts

## Quick Start
1. Run setup.bat or setup.ps1 to install dependencies
2. Launch the application:
   - Web interface: Choose option 1 in setup menu
   - CLI: Choose option 2 in setup menu or run directly:
     python generate.py --template document_templates/base.md --client clientA

## Example Output
Generated document for clientA:

# Service Overview

Our system provides AI-driven analytics for retail optimization.

## Key Features

- Real-time inventory tracking
- Predictive demand forecasting
- Automated supplier recommendations

## Contact Information

For more information, please contact:
Acme Corp
Email: info@acmecorp.com
Phone: +1-800-123-4567

## Tagline

Precision Delivered.