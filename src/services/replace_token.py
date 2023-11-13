import json
import os

# Input your OpenAI API key
api_key = os.environ.get("OPENAI_API_TOKEN")

if api_key is not None:
    # File path
    file_path = ".well-known/ai-plugin.json"  # Please replace your_file_name with your file name

    # Read JSON file
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Replace API key
    data["auth"]["verification_tokens"]["openai"] = api_key

    # Write the modified data back to the JSON file
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
