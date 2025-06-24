import os
import ctypes

HOSTS_PATH = r"C:\Windows\System32\drivers\etc\hosts"

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def add_host_entry(domain):
    entry = f"127.0.0.1    {domain}\n"
    with open(HOSTS_PATH, "r") as file:
        lines = file.readlines()

    if any(domain in line for line in lines):
        print(f"{domain} already exists in hosts file.")
        return

    with open(HOSTS_PATH, "a") as file:
        file.write(entry)
    print(f"✅ Added {entry.strip()} to hosts file.")

if __name__ == "__main__":
    if not is_admin():
        print("❌ Run this script as administrator.")
    else:
        tenant_domain = input("Enter the tenant domain (e.g. tenant1.localhost): ").strip()
        if tenant_domain:
            add_host_entry(tenant_domain)
        else:
            print("❌ No domain entered. Exiting.")
