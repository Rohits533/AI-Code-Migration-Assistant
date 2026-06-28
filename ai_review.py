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

        # 1. Properly structured prompt with closed triple quotes
        prompt = f"""
You are a senior code reviewer. Compare the original and migrated code.
Provide a clear summary of changes, potential bugs, and optimization suggestions.

Original Code:
```python
{original_code}
