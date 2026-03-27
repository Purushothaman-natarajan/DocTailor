import json
import re
from typing import Dict, Any, Optional

class RuleUpdater:
    """Applies rules to template content."""
    
    def __init__(self):
        pass
    
    def apply_terminology_rules(self, content: str, terminology_rules: Dict[str, Any]) -> str:
        """Apply terminology replacement rules."""
        if not terminology_rules or "replace" not in terminology_rules:
            return content
        
        replacements = terminology_rules["replace"]
        updated_content = content
        
        for old_term, new_term in replacements.items():
            # Use word boundaries to avoid partial replacements
            pattern = r'\b' + re.escape(old_term) + r'\b'
            updated_content = re.sub(pattern, new_term, updated_content, flags=re.IGNORECASE)
        
        return updated_content
    
    def apply_branding_rules(self, content: str, branding_rules: Dict[str, Any]) -> str:
        """Apply branding rules to content."""
        if not branding_rules:
            return content
        
        updated_content = content
        
        # Replace branding placeholders
        for key, value in branding_rules.items():
            placeholder = "{" + key + "}"
            updated_content = updated_content.replace(placeholder, str(value))
        
        return updated_content
    
    def apply_rules(self, content: str, rules: Dict[str, Any]) -> str:
        """Apply all rules to content."""
        updated_content = content
        
        # Apply terminology rules first
        if "terminology" in rules:
            updated_content = self.apply_terminology_rules(updated_content, rules["terminology"])
        
        # Apply branding rules
        if "branding" in rules:
            updated_content = self.apply_branding_rules(updated_content, rules["branding"])
        
        # Apply client-specific rules (direct value replacements)
        if "client" in rules:
            for key, value in rules["client"].items():
                placeholder = "{" + key + "}"
                updated_content = updated_content.replace(placeholder, str(value))
        
        return updated_content