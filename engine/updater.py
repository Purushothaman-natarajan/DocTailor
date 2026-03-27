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
    
    def get_nested_value(self, data: Dict[str, Any], key: str) -> Any:
        """Get a value from a nested dictionary using a dot-separated key.
        
        Args:
            data: The dictionary to search
            key: Dot-separated key (e.g., "user.name")
            
        Returns:
            The value if found, None otherwise
        """
        keys = key.split('.')
        value = data
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return None
        return value
    
    def _get_value_from_sources(self, placeholder: str, rules: Dict[str, Any]) -> Optional[Any]:
        """Get a value for a placeholder from the branding or client sources.
        
        Args:
            placeholder: The placeholder string (without braces)
            rules: The rules dictionary containing 'branding' and/or 'client' keys
            
        Returns:
            The value if found in either branding or client (using dot notation), None otherwise
        """
        # Check if the placeholder specifies a source (branding or client)
        if '.' in placeholder:
            parts = placeholder.split('.', 1)  # Split into [source, rest]
            source = parts[0]
            rest = parts[1]
            if source in ['branding', 'client'] and source in rules:
                return self.get_nested_value(rules[source], rest)
            # If the source is not branding/client or not in rules, fall through to search both
        
        # Try to find in branding first, then client
        if 'branding' in rules:
            value = self.get_nested_value(rules['branding'], placeholder)
            if value is not None:
                return value
        if 'client' in rules:
            value = self.get_nested_value(rules['client'], placeholder)
            if value is not None:
                return value
        return None
    
    def apply_rules(self, content: str, rules: Dict[str, Any]) -> str:
        """Apply all rules to content.
        
        Order of operations:
        1. Apply terminology rules (global string replacements)
        2. Replace placeholders using data from branding and client sections
        
        Args:
            content: The template content
            rules: Dictionary containing 'branding', 'terminology', and/or 'client' keys
            
        Returns:
            Updated content with rules applied
        """
        # Step 1: Apply terminology rules (if present)
        if "terminology" in rules:
            content = self.apply_terminology_rules(content, rules["terminology"])
        
        # Step 2: Extract and replace placeholders
        # We need to get the placeholders from the content after terminology rules
        from engine.parser import TemplateParser
        parser = TemplateParser()
        placeholders = parser.extract_placeholders(content)
        
        # Replace each placeholder with its value from the sources
        for placeholder in placeholders:
            value = self._get_value_from_sources(placeholder, rules)
            if value is not None:
                content = content.replace("{" + placeholder + "}", str(value))
        
        return content
