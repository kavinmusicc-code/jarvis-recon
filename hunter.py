import os, sys, socket, json, time, urllib.request, urllib.error

CONFIG_FILE = os.path.expanduser("~/.jarvis_config.json")

def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                return json.load(f)
        except: pass
    return {"api_key": "", "model": "deepseek/deepseek-chat", "mode": "openclaw-autonomous"}

def save_config(config):
    try:
        with open(CONFIG_FILE, "w") as f:
            json.dump(config, f)
    except: pass

def banner():
    print("="*70)
    print("  JARVIS // OPENCLAW x MYTHOS AI AUTONOMOUS RECON CORE v4.0")
    print("  Status: Neural Mesh Active | Multi-Agent Security Engine Online")
    print("="*70 + "\n")

def call_mythos_ai(prompt, system_instruction="You are Jarvis, powered by OpenClaw and Mythos AI architecture. You provide elite-grade, offensive security reconnaissance and threat mitigation."):
    config = load_config()
    api_key = config.get("api_key")
    if not api_key:
        return "[-] Error: No API Key configured. Use 'setkey <YOUR_API_KEY>' to initialize neural link."
    
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
            "X-Title": "Jarvis OpenClaw Mythos Engine"
        }
    )
    
    try:
        with urllib.request.urlopen(req, timeout=25) as response:
            res = json.loads(response.read().decode("utf-8"))
            return res["choices"][0]["message"]["content"]
    except urllib.error.HTTPError as e:
        return f"[-] API HTTP Error {e.code}: Check your key permissions."
    except Exception as e:
        return f"[-] Neural Link Exception: {e}"

def self_heal_code(error_desc):
    print("\n[*] OpenClaw Self-Healing Engine Triggered...")
    prompt = f"The Python security agent encountered this runtime exception: '{error_desc}'. Provide clean, robust Python code patches to resolve this issue autonomously."
    return call_mythos_ai(prompt, "You are an expert self-healing software architect.")

def scan_target(target):
    print(f"\n[*] Initializing Mythos AI Deep Recon Sweep on target: {target}")
    time.sleep(1)
    ports = [21, 22, 23, 25, 53, 80, 110, 443, 445, 3306, 3389, 8080, 27017]
    open_ports = []
    print("[*] Sweeping high-risk network ports...")
    for p in ports:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.3)
            if s.connect_ex((target, p)) == 0:
                open_ports.append(p)
            s.close()
        except: pass
        print(f"    Port {p} -> Checked", end="\r")
    print(f"\n[+] Sweep Complete. Active Open Ports: {open_ports if open_ports else 'None (Deep Firewalled)'}")
    
    print("\n[*] Dispatching data to Mythos AI & OpenClaw Neural Core...")
    prompt = f"Target: {target}. Detected Open Ports: {open_ports}. Conduct an advanced Mythos-grade security audit, list exploitation vectors, and outline precise remediation steps."
    report = call_mythos_ai(prompt)
    
    print("\n------------------------------------------------------------")
    print(" [!] MYTHOS AI x OPENCLAW RECON INTELLIGENCE REPORT:")
    print("------------------------------------------------------------")
    print(report)
    print("------------------------------------------------------------\n")

def main():
    banner()
    config = load_config()
    if not config.get("api_key"):
        print(" [!] Notice: API key not set. Run 'setkey <API_KEY>' to unlock full Mythos/OpenClaw AI capabilities.\n")
    
    while True:
        try:
            cmd = input("Jarvis-OpenClaw> ").strip()
            if not cmd: continue
            parts = cmd.split()
            action = parts[0].lower()
            
            if action == 'exit':
                print("[*] Terminating agent session. Goodbye!")
                break
            elif action == 'setkey' and len(parts) > 1:
                config["api_key"] = parts[1]
                save_config(config)
                print("[+] API Key successfully configured and secured locally!")
            elif action == 'model' and len(parts) > 1:
                config["model"] = parts[1]
                save_config(config)
                print(f"[+] Active Neural Model switched to: {parts[1]}")
            elif action == 'scan' and len(parts) > 1:
                scan_target(parts[1])
            elif action == 'ask' and len(parts) > 1:
                query = " ".join(parts[1:])
                print("\n[*] Consulting Mythos AI Core...")
                print(call_mythos_ai(query))
                print()
            elif action == 'heal':
                print(self_heal_code("Simulated system exception check."))
            else:
                print("[-] Unknown command. Available commands:")
                print("    - scan <target>         (Run Mythos AI reconnaissance audit)")
                print("    - ask <prompt>          (Consult AI on cybersecurity topics)")
                print("    - setkey <api_key>      (Configure OpenRouter API Key)")
                print("    - model <name>          (Switch LLM model e.g. openai/gpt-4o)")
                print("    - heal                  (Run self-healing diagnostics)")
                print("    - exit                  (Quit session)")
        except KeyboardInterrupt:
            print("\n[*] Session interrupted. Exiting...")
            break
        except Exception as e:
            print(f"[-] Runtime Exception: {e}")
            print(self_heal_code(str(e)))

if __name__ == '__main__':
    main()