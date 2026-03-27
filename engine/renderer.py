import os
from typing import Optional
from .parser import TemplateParser
from .updater import RuleUpdater
from .llm_adapter import get_llm_adapter, LLMAdapter

class TemplateRenderer:
    """Main class for rendering templates with rules and optional LLM enhancement."""
    
    def __init__(self, rules_dir: str = "rules"):
        self.parser = TemplateParser()
        self.updater = RuleUpdater()
        self.rules_dir = rules_dir
    
    def render_template(self, 
                       template_path: str, 
                       client_name: str,
                       llm_provider: Optional[str] = None,
                       llm_api_key: Optional[str] = None,
                       llm_model: Optional[str] = None,
                       llm_instructions: str = "") -> str:
        """
        Render a template for a specific client.
        
        Args:
            template_path: Path to the template file
            client_name: Name of the client (used to load client-specific rules)
            llm_provider: LLM provider (e.g., 'openai', 'anthropic')
            llm_api_key: API key for the LLM provider
            llm_model: Model to use for LLM enhancement
            llm_instructions: Instructions for LLM enhancement
            
        Returns:
            Rendered content as string
        """
        # Parse template
        template_content = self.parser.parse_template(template_path)
        
        # Load rules for this client
        rules = self.parser.load_rules(self.rules_dir, client_name)
        
        # Apply rules
        rendered_content = self.updater.apply_rules(template_content, rules)
        
        # Apply LLM enhancement if requested
        if llm_provider:
            llm_adapter = get_llm_adapter(
                provider=llm_provider,
                api_key=llm_api_key,
                model=llm_model
            )
            rendered_content = llm_adapter.enhance_content(
                rendered_content, 
                instructions=llm_instructions
            )
        
        return rendered_content
    
    def save_output(self, content: str, output_path: str) -> None:
        """Save rendered content to output file."""
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)