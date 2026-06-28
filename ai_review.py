import requests
import json

def review_migration(original_code, migrated_code, api_key):
    """
    Sends original + migrated code to Groq and returns an AI summary of changes.
    """
    try:
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        prompt = f"""
You are a senior code reviewer. Compare the original and migrated code.

Original:
```python
{original_code}
