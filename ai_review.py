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
