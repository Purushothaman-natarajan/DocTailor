import os
import logging
from typing import Optional
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

logger = logging.getLogger(__name__)

class LLMAdapter:
    """Base class for LLM adapters."""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-3.5-turbo"):
        self.api_key = api_key
        self.model = model
    
    def enhance_content(self, content: str, instructions: str = "") -> str:
        """Enhance content using LLM. To be implemented by subclasses."""
        raise NotImplementedError

class OpenAIAdapter(LLMAdapter):
    """OpenAI LLM adapter."""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-3.5-turbo"):
        super().__init__(api_key, model)
        if not self.api_key:
            self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            logger.warning("OpenAI API key not found. LLM enhancement will be skipped.")
    
    def enhance_content(self, content: str, instructions: str = "") -> str:
        """Enhance content using OpenAI API."""
        if not self.api_key:
            logger.warning("OpenAI API key not available. Returning original content.")
            return content
        
        try:
            import openai
            openai.api_key = self.api_key
            
            prompt = f"""
            {instructions}
            
            Content to enhance:
            {content}
            
            Enhanced content:
            """
            
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that enhances document content."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.7
            )
            
            enhanced_content = response.choices[0].message.content.strip()
            return enhanced_content
        except Exception as e:
            logger.error(f"Error enhancing content with OpenAI: {e}")
            return content

class AnthropicAdapter(LLMAdapter):
    """Anthropic Claude LLM adapter."""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "claude-2"):
        super().__init__(api_key, model)
        if not self.api_key:
            self.api_key = os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            logger.warning("Anthropic API key not found. LLM enhancement will be skipped.")
    
    def enhance_content(self, content: str, instructions: str = "") -> str:
        """Enhance content using Anthropic API."""
        if not self.api_key:
            logger.warning("Anthropic API key not available. Returning original content.")
            return content
        
        try:
            import anthropic
            client = anthropic.Anthropic(api_key=self.api_key)
            
            prompt = f"""
            {instructions}
            
            Content to enhance:
            {content}
            
            Enhanced content:
            """
            
            response = client.completions.create(
                model=self.model,
                max_tokens_to_sample=1000,
                prompt=f"{anthropic.HUMAN_PROMPT} {prompt} {anthropic.AI_PROMPT}",
            )
            
            enhanced_content = response.completion.strip()
            return enhanced_content
        except Exception as e:
            logger.error(f"Error enhancing content with Anthropic: {e}")
            return content

class GeminiAdapter(LLMAdapter):
    """Google Gemini LLM adapter."""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gemini-pro"):
        super().__init__(api_key, model)
        if not self.api_key:
            self.api_key = os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            logger.warning("Google API key not found. LLM enhancement will be skipped.")
    
    def enhance_content(self, content: str, instructions: str = "") -> str:
        """Enhance content using Google Gemini API."""
        if not self.api_key:
            logger.warning("Google API key not available. Returning original content.")
            return content
        
        try:
            import google.generativeai as genai
            genai.configure(api_key=self.api_key)
            
            # Set up the model
            model = genai.GenerativeModel(self.model)
            
            prompt = f"""
            {instructions}
            
            Content to enhance:
            {content}
            
            Enhanced content:
            """
            
            response = model.generate_content(prompt)
            enhanced_content = response.text.strip()
            return enhanced_content
        except Exception as e:
            logger.error(f"Error enhancing content with Gemini: {e}")
            return content

def get_llm_adapter(provider: str, api_key: Optional[str] = None, model: Optional[str] = None) -> LLMAdapter:
    """Factory function to get LLM adapter instance."""
    provider = provider.lower()
    
    if provider == "openai" or provider.startswith("gpt"):
        # Default model for OpenAI
        model = model or "gpt-3.5-turbo"
        return OpenAIAdapter(api_key=api_key, model=model)
    elif provider == "anthropic" or provider.startswith("claude"):
        # Default model for Anthropic
        model = model or "claude-2"
        return AnthropicAdapter(api_key=api_key, model=model)
    elif provider == "google" or provider.startswith("gemini"):
        # Default model for Gemini
        model = model or "gemini-pro"
        return GeminiAdapter(api_key=api_key, model=model)
    else:
        logger.warning(f"Unknown LLM provider: {provider}. Returning a dummy adapter that does nothing.")
        # Return a dummy adapter that just returns the content
        class DummyAdapter(LLMAdapter):
            def enhance_content(self, content: str, instructions: str = "") -> str:
                return content
        return DummyAdapter()
