import json
import requests
import re
import sys
sys.path.append("/Users/sadanandupase/PycharmProjects/23AI")
print(sys.path)
import array
from embeddings.generate_embeddings import generate_embeddings

OLLAMA_URL = "http://localhost:11434/api/chat"
MCP_URL = "http://localhost:8000/mcp/run"

def call_llm_ollama(prompt, vec):
    system_prompt = open("prompt/system_prompt.txt").read()

    response = requests.post(OLLAMA_URL, json={
        "model": "llama3.2",  # or llama3, phi3, etc.
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        "stream": False
    })

    if response.status_code != 200:
        print("Error from Ollama:", response.text)
        return None
    print(response.json())
    content = response.json()["message"]["content"]
    return fix_llm_json(content, vec)

def fix_llm_json(text, vec):
    """
    Fix and parse JSON output from LLMs that might include:
    - Markdown code block (```json ... ```)
    - Escaped newlines (\n)
    - Single quotes
    - Trailing commas
    """
    import re

    # Remove markdown-style code block wrappers like ```json ... ```
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)


    # Try loading raw text first
    try:
        data = json.loads(text)
        #making sure we pass embedding only when required
        if vec and 'VECTOR_DISTANCE' in data['query']:
            data["embedding"] = list(vec)
        return data
    except json.JSONDecodeError:
        pass

    # Try to clean and fix common issues
    try:
        # Replace escaped newlines with actual ones
        text = text.replace("\\n", "\n")

        # Try to extract { ... } block only
        match = re.search(r'{.*}', text, re.DOTALL)
        if not match:
            raise ValueError("No valid JSON object found")

        json_text = match.group(0)

        # Common fixes
        json_text = json_text.replace("'", '"')  # single → double quotes
        json_text = re.sub(r',\s*([}\]])', r'\1', json_text)  # remove trailing commas

        data = json.loads(json_text)
        if vec:
            data["embedding"] = list(vec)
        return data
    except Exception as e:
        raise ValueError(f"⚠️ Failed to fix and parse JSON: {e}\nRaw text:\n{text}")



def call_mcp(json_payload):
    resp = requests.post("http://localhost:8000/mcp/run", json=json_payload)
    return resp.json()


if __name__ == "__main__":
    while True:
        user_input = input("Ask your DB: ")
        if str.upper(user_input.strip("")) == "EXIT":
            break
        query_embeddings = generate_embeddings(user_input)
        if query_embeddings:
            emb_list = query_embeddings.embeddings[0]
        else:
            emb_list = None
        if emb_list:
            vec = array.array("f", emb_list)
        else:
            vec = None
        llm_response = call_llm_ollama(user_input, vec)
        print("LLM says:", llm_response)

        try:
            parsed = llm_response  # Better: use json.loads() if response is well-formed
            result = call_mcp(parsed)
            print("MCP Result:", result)
        except Exception as e:
            print("Error parsing or calling MCP:", e)
