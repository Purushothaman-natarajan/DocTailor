#!/usr/bin/env python3
"""
DocTailor Web Interface - Flask application for document generation.
"""

from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import sys
import json
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from engine.renderer import TemplateRenderer

app = Flask(__name__, static_folder='../static', template_folder='../web_templates')

# Initialize renderer
renderer = TemplateRenderer()

# Serve frontend files
@app.route('/')
def index():
    """Render the main page."""
    return send_from_directory('../frontend', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    """Serve static files from frontend directory."""
    return send_from_directory('../frontend', path)

# API Routes
@app.route('/templates')
def get_templates():
    """Get available templates."""
    try:
        templates = []
        if os.path.exists('document_templates'):
            templates = [f for f in os.listdir('document_templates') 
                        if f.endswith(('.md', '.txt', '.template'))]
        return jsonify(templates)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/clients')
def get_clients():
    """Get available clients."""
    try:
        clients = []
        if os.path.exists('rules'):
            clients = [f.replace('.json', '') for f in os.listdir('rules') 
                      if f.endswith('.json') and f not in ['branding.json', 'terminology.json']]
        return jsonify(clients)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/rules/<client_name>')
def get_client_rules(client_name):
    """Get rules for a specific client."""
    try:
        rules_path = os.path.join('rules', f'{client_name}.json')
        if os.path.exists(rules_path):
            with open(rules_path, 'r') as f:
                rules = json.load(f)
            return jsonify(rules)
        else:
            return jsonify({}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/generate', methods=['POST'])
def generate_document():
    """Generate a document based on form data."""
    try:
        data = request.json
        template_name = data.get('template')
        client_name = data.get('client')
        llm_provider = data.get('llm')
        llm_model = data.get('llm_model')
        llm_instructions = data.get('llm_instructions', '')
        
        if not template_name or not client_name:
            return jsonify({'error': 'Template and client are required'}), 400
        
        template_path = os.path.join('document_templates', template_name)
        if not os.path.exists(template_path):
            return jsonify({'error': f'Template not found: {template_name}'}), 404
        
        # Render template
        rendered_content = renderer.render_template(
            template_path=template_path,
            client_name=client_name,
            llm_provider=llm_provider,
            llm_model=llm_model,
            llm_instructions=llm_instructions
        )
        
        # Save output
        output_dir = os.path.join('clients', client_name)
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, template_name)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(rendered_content)
        
        return jsonify({
            'success': True,
            'message': f'Document generated successfully',
            'output_path': output_path,
            'content': rendered_content
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/preview', methods=['POST'])
def preview_document():
    """Preview a document without saving."""
    try:
        data = request.json
        template_name = data.get('template')
        client_name = data.get('client')
        llm_provider = data.get('llm')
        llm_model = data.get('llm_model')
        llm_instructions = data.get('llm_instructions', '')
        
        if not template_name or not client_name:
            return jsonify({'error': 'Template and client are required'}), 400
        
        template_path = os.path.join('document_templates', template_name)
        if not os.path.exists(template_path):
            return jsonify({'error': f'Template not found: {template_name}'}), 404
        
        # Render template
        rendered_content = renderer.render_template(
            template_path=template_path,
            client_name=client_name,
            llm_provider=llm_provider,
            llm_model=llm_model,
            llm_instructions=llm_instructions
        )
        
        return jsonify({
            'success': True,
            'content': rendered_content
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)