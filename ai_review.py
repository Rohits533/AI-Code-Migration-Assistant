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
Provide a clear summary of changes, potential bugs, and optimization suggestions.

Original Code:
```python
{original_code}
```

Migrated Code:
```python
{migrated_code}
```
"""

        data = {
            "model": "llama3-8b-8192",
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.2
        }

        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()

        response_json = response.json()
        return response_json["choices"][0]["message"]["content"]

    except requests.exceptions.RequestException as e:
        return f"API Error: {str(e)}"
    except KeyError:
        return "Error: Unexpected response format from the API."
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"
