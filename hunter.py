import os, sys, socket, json, time
import urllib.request
import urllib.error

CONFIG_FILE = os.path.expanduser("~/.jarvis_config.json")

def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                return json.load(f)
        except: pass
    return {"api_key": "", "provider": "openrouter"}

def save_config(config):
    try:
        with open(CONFIG_FILE, "w") as f:
            json.dump(config, f)
    except: pass

def banner():
    print("="*65)
    print("  JARVIS // AI-POWERED AUTONOMOUS BUG HUNTER & RECON AGENT")
    print("  Status: Universal Recon & LLM Security Core Active")
    print("="*65 + "\n")

def call_ai_analyst(target, open_ports, api_key):
    print(f"\n[*] Connecting to Neural Core (LLM) using provided API Key...")
    prompt = f"Perform a professional cybersecurity reconnaissance analysis for target: {target}. Open ports detected: {open_ports}. Provide short, high-impact security risks and actionable remediation steps in bullet points."
    
    payload = {
        "model": "deepseek/deepseek-chat", # or any default openrouter model
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.3
    }
    
    req_data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        "https://openrouter.ai/api/v1/chat/completions",
        data=req_data,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://jarvis-recon.vercel.app",
            "X-Title": "Jarvis Recon Agent"
        }
    )
    
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            res = json.loads(response.read().decode("utf-8"))
            content = res["choices"][0]["message"]["content"]
            return content
    except urllib.error.HTTPError as e:
        return f"[-] AI API Error (HTTP {e.code}): Check if your API Key is valid."
    except Exception as e:
        return f"[-] Connection Error: {e}"

def scan_target(target):
    print(f"\n[*] Initiating deep reconnaissance probe on target: {target}")
    time.sleep(1)
    ports = [21, 22, 80, 443, 8080, 3306, 27017]
    open_ports = []
    print("[*] Scanning common high-risk ports...")
    for p in ports:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.4)
            if s.connect_ex((target, p)) == 0:
                open_ports.append(p)
            s.close()
        except: pass
        print(f"    Port {p} -> Checked", end="\r")
    print(f"\n[+] Scan Complete. Open Ports Detected: {open_ports if open_ports else 'None (Firewalled)'}")
    
    config = load_config()
    if config.get("api_key"):
        print("\n[+] AI API Key found! Requesting deep threat intelligence analysis...")
        ai_report = call_ai_analyst(target, open_ports, config["api_key"])
        print("\n------------------------------------------------------------")
        print(" [!] AI-POWERED SECURITY RECON REPORT:")
        print("------------------------------------------------------------")
        print(ai_report)
        print("------------------------------------------------------------\n")
    else:
        print("\n------------------------------------------------------------")
        print(" [!] LOCAL VULNERABILITY ASSESSMENT REPORT:")
        print("------------------------------------------------------------")
        if open_ports:
            print(" -> Warning: Open HTTP/HTTPS or Database ports exposed.")
            print(" -> Recommendation: Enforce strict rate-limiting and WAF protection.")
        else:
            print(" -> Target appears heavily fortified. No critical vector found.")
        print(" [i] Tip: Set your AI API key using 'setkey <YOUR_API_KEY>' for deep LLM analysis.")
        print("------------------------------------------------------------\n")

def main():
    banner()
    while True:
        try:
            cmd = input("Hunter-CLI> ").strip()
            if not cmd:
                continue
            parts = cmd.split()
            action = parts[0].lower()
            
            if action == 'exit':
                print("[*] Terminating Hunter session.")
                break
            elif action == 'setkey' and len(parts) > 1:
                key = parts[1]
                config = load_config()
                config["api_key"] = key
                save_config(config)
                print("[+] API Key successfully saved to secure local config!")
            elif action == 'scan' and len(parts) > 1:
                scan_target(parts[1])
            else:
                print("[-] Unknown command.")
                print("    Available commands:")
                print("    - scan <target>          (Run port scan & security assessment)")
                print("    - setkey <api_key>       (Configure your custom AI API Key)")
                print("    - exit                   (Quit agent)")
        except KeyboardInterrupt:
            print("\n[*] Exiting...")
            break
        except Exception as e:
            print(f"[-] Error: {e}")

if __name__ == '__main__':
    main()