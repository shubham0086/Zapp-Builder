from typing import Dict, List, Any, Optional
import openai
from anthropic import Anthropic
import httpx
from ..core.config import settings
from loguru import logger

class LLMService:
    """Service for managing different LLM providers"""
    
    def __init__(self):
        self.openai_client = None
        self.anthropic_client = None
        
        # Initialize clients based on available API keys
        if settings.OPENAI_API_KEY:
            self.openai_client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
            logger.info("✅ OpenAI client initialized")
        
        if settings.ANTHROPIC_API_KEY:
            self.anthropic_client = Anthropic(api_key=settings.ANTHROPIC_API_KEY)
            logger.info("✅ Anthropic client initialized")
    
    async def generate_completion(
        self, 
        prompt: str, 
        model: str = "gpt-4-turbo-preview",
        max_tokens: int = 1000,
        temperature: float = 0.7,
        provider: str = "openai"
    ) -> Dict[str, Any]:
        """Generate completion using specified LLM provider"""
        
        try:
            if provider == "openai" and self.openai_client:
                response = self.openai_client.chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=max_tokens,
                    temperature=temperature
                )
                
                return {
                    "success": True,
                    "content": response.choices[0].message.content,
                    "provider": "openai",
                    "model": model,
                    "tokens_used": response.usage.total_tokens
                }
            
            elif provider == "anthropic" and self.anthropic_client:
                response = self.anthropic_client.messages.create(
                    model="claude-3-sonnet-20240229",
                    max_tokens=max_tokens,
                    temperature=temperature,
                    messages=[{"role": "user", "content": prompt}]
                )
                
                return {
                    "success": True,
                    "content": response.content[0].text,
                    "provider": "anthropic",
                    "model": "claude-3-sonnet-20240229",
                    "tokens_used": response.usage.input_tokens + response.usage.output_tokens
                }
            
            else:
                return {
                    "success": False,
                    "error": f"Provider {provider} not available or not configured",
                    "content": "",
                    "tokens_used": 0
                }
        
        except Exception as e:
            logger.error(f"LLM generation failed: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "content": "",
                "tokens_used": 0
            }
    
    def get_available_providers(self) -> List[str]:
        """Get list of available LLM providers"""
        providers = []
        if self.openai_client:
            providers.append("openai")
        if self.anthropic_client:
            providers.append("anthropic")
        return providers
    
    def estimate_tokens(self, text: str) -> int:
        """Estimate token count for text (rough approximation)"""
        # Rough estimation: ~4 characters per token
        return len(text) // 4