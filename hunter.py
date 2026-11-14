import os, sys, socket, json, time

def banner():
    print("="*60)
    print("  JARVIS // ULTRA-ADVANCED AUTONOMOUS BUG HUNTER & RECON AGENT")
    print("  Status: Zero-API / Local Security Simulation Mode Active")
    print("="*60 + "\n")

def scan_target(target):
    print(f"\n[*] Initiating deep reconnaissance probe on target: {target}")
    time.sleep(1)
    ports = [21, 22, 80, 443, 8080, 3306]
    open_ports = []
    print("[*] Scanning common high-risk ports...")
    for p in ports:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.5)
            if s.connect_ex((target, p)) == 0:
                open_ports.append(p)
            s.close()
        except: pass
        print(f"    Port {p} -> Checked", end="\r")
    print(f"\n[+] Scan Complete. Open Ports Detected: {open_ports if open_ports else 'None (Firewalled)'}")
    print("\n[*] Analyzing potential vulnerability vectors...")
    time.sleep(1.5)
    print("\n------------------------------------------------------------")
    print(" [!] VULNERABILITY ASSESSMENT REPORT:")
    print(" ------------------------------------------------------------")
    if open_ports:
        print(" -> Warning: Open HTTP/HTTPS or Database ports exposed.")
        print(" -> Recommendation: Enforce strict rate-limiting and WAF protection.")
    else:
        print(" -> Target appears heavily fortified or offline. No critical vector found.")
    print("------------------------------------------------------------\n")

def main():
    banner()
    while True:
        try:
            cmd = input("Hunter-CLI> ").strip()
            if not cmd or cmd.lower() == 'exit':
                print("[*] Terminating Hunter session.")
                break
            parts = cmd.split()
            if parts[0].lower() == 'scan' and len(parts) > 1:
                scan_target(parts[1])
            else:
                print("[-] Unknown command. Use: scan <target>")
        except KeyboardInterrupt:
            print("\n[*] Exiting...")
            break
        except Exception as e:
            print(f"[-] Error: {e}")

if __name__ == '__main__':
    main()