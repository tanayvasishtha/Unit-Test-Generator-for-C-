"""
LLM Client for communicating with different AI models
Supports Ollama, OpenAI, and GitHub Models
"""

import requests
import json
import time
from typing import Dict, Optional, Any

class LLMClient:
    """Client for interacting with various LLM providers"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.provider = config['llm_settings']['provider']
        self.request_settings = config['llm_settings'].get('request_settings', {})
        
    def generate(self, prompt: str) -> Optional[str]:
        """Generate text using the configured LLM"""
        max_retries = self.request_settings.get('max_retries', 3)
        retry_delay = self.request_settings.get('retry_delay', 2)
        
        for attempt in range(max_retries):
            try:
                if self.provider == 'ollama':
                    return self._generate_ollama(prompt)
                elif self.provider == 'openai':
                    return self._generate_openai(prompt)
                elif self.provider == 'github':
                    return self._generate_github(prompt)
                else:
                    raise ValueError(f"Unsupported provider: {self.provider}")
                    
            except Exception as e:
                print(f"Attempt {attempt + 1} failed: {e}")
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                else:
                    print(f"All attempts failed for provider: {self.provider}")
                    
        return None
    
    def _generate_ollama(self, prompt: str) -> Optional[str]:
        """Generate using Ollama"""
        config = self.config['llm_settings']['ollama']
        
        url = f"{config['base_url']}/api/generate"
        payload = {
            "model": config['model'],
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": self.request_settings.get('temperature', 0.1),
                "num_predict": self.request_settings.get('max_tokens', 4096)
            }
        }
        
        response = requests.post(
            url, 
            json=payload, 
            timeout=config.get('timeout', 300)
        )
        
        if response.status_code == 200:
            return response.json().get('response', '')
        else:
            raise Exception(f"Ollama API error: {response.status_code}")
    
    def _generate_openai(self, prompt: str) -> Optional[str]:
        """Generate using OpenAI API"""
        import openai
        
        config = self.config['llm_settings']['openai']
        
        try:
            client = openai.OpenAI(api_key=config['api_key'])
            
            response = client.chat.completions.create(
                model=config['model'],
                messages=[{"role": "user", "content": prompt}],
                max_tokens=config.get('max_tokens', 4096),
                temperature=config.get('temperature', 0.1)
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            raise Exception(f"OpenAI API error: {e}")
    
    def _generate_github(self, prompt: str) -> Optional[str]:
        """Generate using GitHub Models"""
        config = self.config['llm_settings']['github']
        
        url = f"{config['base_url']}/chat/completions"
        headers = {
            "Authorization": f"Bearer {config['api_key']}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": config['model'],
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": self.request_settings.get('max_tokens', 4096),
            "temperature": self.request_settings.get('temperature', 0.1)
        }
        
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            raise Exception(f"GitHub API error: {response.status_code}")
    
    def test_connection(self) -> bool:
        """Test if the LLM connection is working"""
        try:
            test_prompt = "Hello, respond with 'OK' if you can see this message."
            response = self.generate(test_prompt)
            return response is not None and len(response.strip()) > 0
        except:
            return False 