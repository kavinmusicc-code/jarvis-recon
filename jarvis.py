import os
import sys
import json
import urllib.request

def run_jarvis():
    print("==================================================")
    print("  JARVIS // Local Autonomous CLI Agent (BYOK)")
    print("==================================================")
    
    api_key = os.environ.get("JARVIS_API_KEY")
    if not api_key:
        api_key = input("Enter your DeepSeek / OpenAI API Key: ").strip()
        if not api_key:
            print("Error: API Key is required to run Jarvis.")
            return

    print("\n[Status] Jarvis is online and connected via your BYOK key.")
    print("Type your commands below (type 'exit' to quit).\n")

    while True:
        try:
            prompt = input("Jarvis> ").strip()
            if not prompt or prompt.lower() == 'exit':
                print("Shutting down Jarvis. Goodbye!")
                break

            payload = {
                "model": "deepseek-chat",
                "messages": [{"role": "user", content: prompt}],
                "stream": False
            }

            req = urllib.request.Request(
                "https://api.deepseek.com/chat/completions",
                data=json.dumps(payload).encode('utf-8'),
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {api_key}"
                }
            )

            print("Thinking...", end="\r")
            with urllib.request.urlopen(req) as response:
                res_data = json.loads(response.read().decode('utf-8'))
                reply = res_data['choices'][0]['message']['content']
                print("\n--- Jarvis Response ---")
                print(reply)
                print("-----------------------\n")

        except Exception as e:
            print(f"\n[Error] Failed to execute: {e}\n")

if __name__ == "__main__":
    run_jarvis()
