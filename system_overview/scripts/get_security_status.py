import subprocess
import json

def command_exists(command):
    try:
        subprocess.run(["which", command], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def run_command(command):
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return result.stdout.strip()

def get_network_security_status():
    firewall_status = run_command(["ufw", "status"]) if command_exists("ufw") else "UFW not installed"
    vpn_status = run_command(["systemctl", "is-active", "openvpn"]) if command_exists("openvpn") else "OpenVPN not installed"
    tor_status = run_command(["systemctl", "is-active", "tor"]) if command_exists("tor") else "Tor not installed"
    ports_status = run_command(["netstat", "-lntu"]) if command_exists("netstat") else "Netstat not installed"
    ipv6_status = run_command(["sysctl", "-n", "net.ipv6.conf.all.disable_ipv6"]) if command_exists("sysctl") else "Sysctl not installed"

    return {"Network Security Status":{
        "Firewall": firewall_status,
        "VPN": vpn_status,
        "TOR": tor_status,
        "ports": ports_status,
        "ipv6": "Enable" if ipv6_status == "0" else "Disabled" 
    }}

def get_installed_security_modules():
    antivirus_command = "clamscan"
    selinux_command = "sestatus"

    security_status = {}

    if command_exists(antivirus_command):
        antivirus_status = run_command([antivirus_command, "--version"])
        security_status["antivirus"] = antivirus_status
    else:
        security_status["antivirus"] = "ClamAV not installed"

    if command_exists(selinux_command):
        selinux_status = run_command([selinux_command])
        security_status["selinux"] = selinux_status
    else:
        security_status["selinux"] = "SELinux not installed"

    return {"Installed Security Modules":security_status}

def get_user_access_status():
    logged_in_users = run_command(["who"]) if command_exists("who") else "Who command not installed"
    ssh_status = run_command(["systemctl", "is-active", "ssh"]) if command_exists("systemctl") else "Systemctl command not installed"

    return {"User Access Status":{
        "logged_in_users": logged_in_users,
        "ssh_status": ssh_status,
    }}

def get_application_security_status():
    try:
        result = subprocess.run(
            "ls -lt --time=atime /var/lib/dpkg/info | grep -E 'list$' | head -n 1 | awk '{print $6, $7, $8}'",
            shell=True,
            check=True,
            text=True,
            stdout=subprocess.PIPE
        )
        last_update_time = result.stdout.strip()
        # return last_update_time
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        # return None
    
    return {"Application Security Status":{
        "last_update": last_update_time,
    }}

if __name__ == "__main__":
    security_status = {
        "network_security": get_network_security_status(),
        "installed_security_modules": get_installed_security_modules(),
        "user_access_status": get_user_access_status(),
        "application_security_status": get_application_security_status(),
    }

    with open("security_status.json", "w") as json_file:
        json.dump(security_status, json_file, indent=4)

    print("Security status has been saved to security_status.json.")
