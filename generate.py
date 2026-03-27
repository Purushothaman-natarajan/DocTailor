#!/usr/bin/env python3
"""
DocTailor CLI - Generate client-specific documents from templates.
"""

import argparse
import os
import sys
from engine.renderer import TemplateRenderer

def main():
    parser = argparse.ArgumentParser(description="Generate client-specific documents from templates")
    parser.add_argument("--template", required=False, help="Path to template file")
    parser.add_argument("--client", required=False, help="Client name")
    parser.add_argument("--rules-dir", default="rules", help="Directory containing rule files")
    parser.add_argument("--output", help="Output file path (default: clients/<client>/<template_name>)")
    parser.add_argument("--llm", help="LLM provider to use (e.g., openai, anthropic)")
    parser.add_argument("--llm-model", help="LLM model to use")
    parser.add_argument("--llm-instructions", default="", help="Instructions for LLM enhancement")
    parser.add_argument("--list-clients", action="store_true", help="List available clients")
    parser.add_argument("--list-templates", action="store_true", help="List available templates")
    
    args = parser.parse_args()
    
    # Initialize renderer
    renderer = TemplateRenderer(rules_dir=args.rules_dir)
    
    # Handle list commands
    if args.list_clients:
        if os.path.exists(args.rules_dir):
            clients = [f.replace(".json", "") for f in os.listdir(args.rules_dir) 
                      if f.endswith(".json") and f not in ["branding.json", "terminology.json"]]
            print("Available clients:")
            for client in clients:
                print(f"  - {client}")
        else:
            print(f"Rules directory '{args.rules_dir}' not found.")
        return
    
    if args.list_templates:
        templates_dir = "templates"
        if os.path.exists(templates_dir):
            templates = [f for f in os.listdir(templates_dir) 
                        if f.endswith((".md", ".txt", ".template"))]
            print("Available templates:")
            for template in templates:
                print(f"  - {template}")
        else:
            print(f"Templates directory '{templates_dir}' not found.")
        return
    
    # Validate template file
    if not os.path.exists(args.template):
        print(f"Error: Template file '{args.template}' not found.")
        sys.exit(1)
    
    # Determine output path
    if args.output:
        output_path = args.output
    else:
        template_name = os.path.basename(args.template)
        client_dir = os.path.join("clients", args.client)
        output_path = os.path.join(client_dir, template_name)
    
    try:
        # Render template
        rendered_content = renderer.render_template(
            template_path=args.template,
            client_name=args.client,
            llm_provider=args.llm,
            llm_model=args.llm_model,
            llm_instructions=args.llm_instructions
        )
        
        # Save output
        renderer.save_output(rendered_content, output_path)
        print(f"Generated document saved to: {output_path}")
        
    except Exception as e:
        print(f"Error generating document: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()