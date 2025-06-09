#!/usr/bin/env python3
"""
Azure OpenAI Terminal Test Script
Usage: python test_openai.py "your prompt here"
"""

import os
import sys
from dotenv import load_dotenv
import openai

def load_azure_openai():
    """Load Azure OpenAI configuration from .env file"""
    load_dotenv()
    
    api_key = os.getenv('AZURE_OPENAI_API_KEY')
    endpoint = os.getenv('AZURE_OPENAI_ENDPOINT')
    api_version = os.getenv('AZURE_OPENAI_API_VERSION', '2024-02-15-preview')
    deployment_name = os.getenv('AZURE_OPENAI_DEPLOYMENT_NAME', 'o4-mini')
    
    if not api_key or not endpoint:
        raise ValueError("Missing AZURE_OPENAI_API_KEY or AZURE_OPENAI_ENDPOINT in .env file")
    
    return openai.AzureOpenAI(
        api_key=api_key,
        api_version=api_version,
        azure_endpoint=endpoint
    ), deployment_name

def test_connection():
    """Test Azure OpenAI connection"""
    try:
        client, deployment_name = load_azure_openai()
        
        response = client.chat.completions.create(
            model=deployment_name,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Say 'Azure OpenAI connection successful!' and tell me what model you are."}
            ],
            max_tokens=150
        )
        
        print("✅ Connection successful!")
        print(f"📋 Model: {deployment_name}")
        print(f"💬 Response: {response.choices[0].message.content}")
        return True
        
    except Exception as e:
        print(f"❌ Connection failed: {str(e)}")
        return False

def chat_with_ai(prompt):
    """Send a prompt to Azure OpenAI"""
    try:
        client, deployment_name = load_azure_openai()
        
        response = client.chat.completions.create(
            model=deployment_name,
            messages=[
                {"role": "system", "content": "You are a helpful coding assistant that can help with debugging, code analysis, and programming questions."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,
            temperature=0.7
        )
        
        print(f"🤖 {deployment_name}: {response.choices[0].message.content}")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) == 1:
        # No arguments - test connection
        print("🧪 Testing Azure OpenAI connection...")
        test_connection()
    elif sys.argv[1] == "test":
        # Test command
        test_connection()
    else:
        # Use the rest as a prompt
        prompt = " ".join(sys.argv[1:])
        print(f"📝 Prompt: {prompt}")
        print("=" * 50)
        chat_with_ai(prompt)
