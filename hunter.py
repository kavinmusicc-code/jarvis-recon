import os, sys, socket, json, time, urllib.request, urllib.error, datetime

# Omega Alien Claw Autonomous Vault Directory
VAULT_DIR = os.path.expanduser("~/.omega_alien_claw")
CONFIG_FILE = os.path.join(VAULT_DIR, "config.json")
HISTORY_FILE = os.path.join(VAULT_DIR, "execution_history.log")

def init_vault():
    if not os.path.exists(VAULT_DIR):
        try:
            os.makedirs(VAULT_DIR)
        except: pass

def log_activity(action_type, details):
    init_vault()
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] [{action_type.upper()}] {details}\n"
    try:
        with open(HISTORY_FILE, "a", encoding="utf-8") as f:
            f.write(log_entry)
    except: pass

def load_config():
    init_vault()
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except: pass
    return {"api_key": "", "model": "deepseek/deepseek-chat", "mode": "omega-multiverse-autonomous"}

def save_config(config):
    init_vault()
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(config, f)
    except: pass

def banner():
    print("="*75)
    print("  OMEGA ALIEN CLAW // Multiverse Neural Core v10.5")
    print(f"  Status: Autonomous Vault Active -> {VAULT_DIR}")
    print("="*75 + "\n")

def call_omega_ai(prompt, system_instruction="You are Omega Alien Claw, an elite autonomous multi-dimensional security agent powered by advanced neural architecture."):
    config = load_config()
    api_key = config.get("api_key")
    if not api_key:
        return "[-] Error: No Neural API Key configured. Use 'setkey <YOUR_API_KEY>' to link dimensions."
    
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
            "HTTP-Referer": "https://omega-alien-claw.vercel.app",
            "X-Title": "Omega Alien Claw Multiverse Engine"
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
    log_activity("self_heal", f"Triggered due to: {error_desc}")
    print("\n[*] Omega Self-Healing Engine Triggered...")
    prompt = f"The Python security agent encountered this runtime exception: '{error_desc}'. Provide clean, robust Python code patches to resolve this issue autonomously."
    return call_omega_ai(prompt, "You are an expert self-healing software architect.")

def scan_target(target):
    print(f"\n[*] Initializing Omega Deep Recon Sweep on target: {target}")
    log_activity("scan_start", f"Target: {target}")
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
    
    print("\n[*] Dispatching data to Omega Alien Neural Core...")
    prompt = f"Target: {target}. Detected Open Ports: {open_ports}. Conduct an advanced Omega-grade security audit, list exploitation vectors, and outline precise remediation steps."
    report = call_omega_ai(prompt)
    
    # Save report inside the vault folder automatically
    report_filename = os.path.join(VAULT_DIR, f"report_{target.replace('.', '_')}_{int(time.time())}.txt")
    try:
        with open(report_filename, "w", encoding="utf-8") as rf:
            rf.write(report)
        print(f"[+] Report automatically saved to local vault: {report_filename}")
        log_activity("scan_saved", f"Report saved at {report_filename}")
    except Exception as ex:
        print(f"[-] Failed to save report locally: {ex}")

    print("\n------------------------------------------------------------")
    print(" [!] OMEGA ALIEN CLAW RECON INTELLIGENCE REPORT:")
    print("------------------------------------------------------------")
    print(report)
    print("------------------------------------------------------------\n")

def main():
    init_vault()
    banner()
    config = load_config()
    if not config.get("api_key"):
        print(" [!] Notice: API key not set. Run 'setkey <API_KEY>' to unlock full Omega AI capabilities.\n")
    
    while True:
        try:
            cmd = input("Omega-Alien-Claw> ").strip()
            if not cmd: continue
            log_activity("command", cmd)
            parts = cmd.split()
            action = parts[0].lower()
            
            if action == 'exit':
                print("[*] Terminating agent session. Goodbye!")
                log_activity("session", "Terminated")
                break
            elif action == 'setkey' and len(parts) > 1:
                config["api_key"] = parts[1]
                save_config(config)
                print("[+] API Key successfully configured and secured in local vault!")
                log_activity("config", "API Key updated")
            elif action == 'model' and len(parts) > 1:
                config["model"] = parts[1]
                save_config(config)
                print(f"[+] Active Neural Model switched to: {parts[1]}")
                log_activity("config", f"Model switched to {parts[1]}")
            elif action == 'scan' and len(parts) > 1:
                scan_target(parts[1])
            elif action == 'ask' and len(parts) > 1:
                query = " ".join(parts[1:])
                print("\n[*] Consulting Omega Alien Core...")
                res = call_omega_ai(query)
                print(res)
                print()
                log_activity("ask", f"Query: {query}")
            elif action == 'heal':
                print(self_heal_code("Simulated system exception check."))
            elif action == 'vault':
                print(f"\n[+] Local Secure Vault Location: {VAULT_DIR}")
                print(f"[+] Execution History Log: {HISTORY_FILE}\n")
            else:
                print("[-] Unknown command. Available commands:")
                print("    - scan <target>         (Run Omega AI reconnaissance audit)")
                print("    - ask <prompt>          (Consult AI on cybersecurity topics)")
                print("    - setkey <api_key>      (Configure OpenRouter API Key)")
                print("    - model <name>          (Switch LLM model e.g. openai/gpt-4o)")
                print("    - heal                  (Run self-healing diagnostics)")
                print("    - vault                 (Check local vault path and logs)")
                print("    - exit                  (Quit session)")
        except KeyboardInterrupt:
            print("\n[*] Session interrupted. Exiting...")
            break
        except Exception as e:
            print(f"[-] Runtime Exception: {e}")
            print(self_heal_code(str(e)))

if __name__ == '__main__':
    main()