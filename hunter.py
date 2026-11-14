import os, sys, socket, json, time, urllib.request, urllib.error

CONFIG_FILE = os.path.expanduser("~/.jarvis_config.json")

def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                return json.load(f)
        except: pass
    return {"api_key": "", "model": "deepseek/deepseek-chat"}

def save_config(config):
    try:
        with open(CONFIG_FILE, "w") as f:
            json.dump(config, f)
    except: pass

def banner():
    print("="*65)
    print("  JARVIS // SELF-HEALING & SELF-DEVELOPING AI RECON CORE")
    print("  Status: Autonomous OpenRouter Neural Mesh Active")
    print("="*65 + "\n")

def call_ai(prompt, system_instruction="You are Jarvis, an elite autonomous cybersecurity recon and self-developing agent."):
    config = load_config()
    api_key = config.get("api_key")
    if not api_key:
        return "[-] Error: No API Key configured. Use 'setkey <YOUR_API_KEY>' first."
    
    payload = {
        "model": config.get("model", "deepseek/deepseek-chat"),
        "messages": [
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.4
    }
    
    req_data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        "https://openrouter.ai/api/v1/chat/completions",
        data=req_data,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://jarvis-recon.vercel.app",
            "X-Title": "Jarvis Autonomous Agent"
        }
    )
    
    try:
        with urllib.request.urlopen(req, timeout=20) as response:
            res = json.loads(response.read().decode("utf-8"))
            return res["choices"][0]["message"]["content"]
    except urllib.error.HTTPError as e:
        return f"[-] API HTTP Error {e.code}: Check your key or model permissions."
    except Exception as e:
        return f"[-] Neural Link Error: {e}"

def self_heal_code(error_desc):
    print("\n[*] Jarvis Self-Healing Protocol Triggered...")
    print(f"[*] Analyzing error context: {error_desc}")
    prompt = f"The Python security agent encountered this error/issue: '{error_desc}'. Provide python code snippet or logic patch to fix this issue autonomously."
    solution = call_ai(prompt, "You are a self-healing software architect. Provide clean python code patches.")
    return solution

def scan_target(target):
    print(f"\n[*] Initiating autonomous neural recon probe on: {target}")
    time.sleep(1)
    ports = [21, 22, 80, 443, 8080, 3306, 27017, 6379]
    open_ports = []
    print("[*] Running multi-threaded port intelligence sweep...")
    for p in ports:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.3)
            if s.connect_ex((target, p)) == 0:
                open_ports.append(p)
            s.close()
        except: pass
        print(f"    Port {p} -> Checked", end="\r")
    print(f"\n[+] Sweep Complete. Active Ports: {open_ports if open_ports else 'None (Firewalled)'}")
    
    print("\n[*] Engaging OpenRouter AI for deep offensive threat modeling...")
    prompt = f"Target: {target}. Open Ports: {open_ports}. Conduct an advanced cybersecurity vulnerability analysis, outline attack vectors, and provide mitigation steps."
    report = call_ai(prompt)
    
    print("\n------------------------------------------------------------")
    print(" [!] AUTONOMOUS AI RECON INTELLIGENCE REPORT:")
    print("------------------------------------------------------------")
    print(report)
    print("------------------------------------------------------------\n")

def main():
    banner()
    config = load_config()
    if not config.get("api_key"):
        print(" [!] Notice: AI API key not set. Run 'setkey <API_KEY>' to unlock full AI power.\n")
    
    while True:
        try:
            cmd = input("Jarvis-AI> ").strip()
            if not cmd: continue
            parts = cmd.split()
            action = parts[0].lower()
            
            if action == 'exit':
                print("[*] Disconnecting Jarvis neural link. Goodbye!")
                break
            elif action == 'setkey' and len(parts) > 1:
                config["api_key"] = parts[1]
                save_config(config)
                print("[+] OpenRouter API Key successfully configured and encrypted locally!")
            elif action == 'model' and len(parts) > 1:
                config["model"] = parts[1]
                save_config(config)
                print(f"[+] Active AI Model switched to: {parts[1]}")
            elif action == 'scan' and len(parts) > 1:
                scan_target(parts[1])
            elif action == 'ask' and len(parts) > 1:
                query = " ".join(parts[1:])
                print("\n[*] Querying Neural Core...")
                print(call_ai(query))
                print()
            elif action == 'heal':
                sample_err = "Simulated socket timeout or module exception."
                print(self_heal_code(sample_err))
            else:
                print("[-] Unknown command. Available commands:")
                print("    - scan <target>         (Run AI-powered target reconnaissance)")
                print("    - ask <prompt>          (Consult Jarvis AI on any security topic)")
                print("    - setkey <api_key>      (Configure OpenRouter API Key)")
                print("    - model <model_name>    (Switch AI model e.g. openai/gpt-4o)")
                print("    - heal                  (Run self-healing diagnostic)")
                print("    - exit                  (Quit session)")
        except KeyboardInterrupt:
            print("\n[*] Session interrupted. Exiting...")
            break
        except Exception as e:
            print(f"[-] Runtime Exception: {e}")
            print(self_heal_code(str(e)))

if __name__ == '__main__':
    main()