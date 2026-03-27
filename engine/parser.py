import os
import json
from typing import Dict, Any, Optional

class TemplateParser:
    """Parses template files and extracts placeholders."""
    
    def __init__(self):
        self.placeholders = {}
    
    def parse_template(self, template_path: str) -> str:
        """Read and parse a template file."""
        if not os.path.exists(template_path):
            raise FileNotFoundError(f"Template not found: {template_path}")
        
        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return content
    
    def extract_placeholders(self, content: str) -> Dict[str, Any]:
        """Extract all placeholders from template content."""
        import re
        
        # Find all placeholders in format {placeholder_name}
        pattern = r'\{([^}]+)\}'
        matches = re.findall(pattern, content)
        
        placeholders = {}
        for match in matches:
            placeholders[match] = None
        
        return placeholders
    
    def load_rules(self, rules_dir: str, client_name: str) -> Dict[str, Any]:
        """Load all rule files for a client."""
        rules = {}
        
        # Load branding rules
        branding_path = os.path.join(rules_dir, "branding.json")
        if os.path.exists(branding_path):
            with open(branding_path, 'r', encoding='utf-8') as f:
                rules["branding"] = json.load(f)
        
        # Load terminology rules
        terminology_path = os.path.join(rules_dir, "terminology.json")
        if os.path.exists(terminology_path):
            with open(terminology_path, 'r', encoding='utf-8') as f:
                rules["terminology"] = json.load(f)
        
        # Load client-specific rules if they exist
        client_rules_path = os.path.join(rules_dir, f"{client_name}.json")
        if os.path.exists(client_rules_path):
            with open(client_rules_path, 'r', encoding='utf-8') as f:
                rules["client"] = json.load(f)
        
        return rules