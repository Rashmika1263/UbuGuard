import subprocess

def get_ssh_status():
    try:
        with open("/var/run/sshd.pid", "r") as pid_file:
            pid = int(pid_file.read().strip())
            return pid is not None
    except FileNotFoundError:
        return False

def enable_ssh():
    try:
        subprocess.run(["sudo", "service", "ssh", "start"], check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def disable_ssh():
    try:
        subprocess.run(["sudo", "service", "ssh", "stop"], check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def restart_ssh():
    try:
        subprocess.run(["sudo", "service", "ssh", "restart"], check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def read_sshd_config(file_path="/etc/ssh/sshd_config"):
    with open(file_path, 'r') as file:
        return file.readlines()

def write_sshd_config(lines, file_path="/etc/ssh/sshd_config"):
    with open(file_path, 'w') as file:
        file.writelines(lines)

def setting_exists(lines, setting):
    for line in lines:
        if line.strip().startswith(setting):
            return True
    return False

def get_boolean_setting(lines, setting):
    for line in lines:
        if line.strip().startswith(setting):
            return line.split()[1].lower() == 'yes'
    return None

def set_boolean_setting(lines, setting, value):
    for i, line in enumerate(lines):
        if line.strip().startswith(setting):
            lines[i] = f"{setting} {'yes' if value else 'no'}\n"
            return
    lines.append(f"{setting} {'yes' if value else 'no'}\n")

def get_list_setting(lines, setting):
    for line in lines:
        if line.strip().startswith(setting):
            return line.split()[1:]
    return []

def set_list_setting(lines, setting, values):
    for i, line in enumerate(lines):
        if line.strip().startswith(setting):
            lines[i] = f"{setting} {' '.join(values)}\n"
            return
    lines.append(f"{setting} {' '.join(values)}\n")

if __name__ == "__main__":
    # # Example usage when running the module as a script
    # sshd_config_lines = read_sshd_config()

    # # Example: Change default port
    # set_boolean_setting(sshd_config_lines, "PermitRootLogin", False)
    # set_boolean_setting(sshd_config_lines, "PasswordAuthentication", True)
    # set_boolean_setting(sshd_config_lines, "UseDNS", False)
    # set_boolean_setting(sshd_config_lines, "PermitEmptyPasswords", False)

    # set_list_setting(sshd_config_lines, "AllowUsers", ["ubuntu"])

    # # Change the default SSH port
    # set_list_setting(sshd_config_lines, "Port", ["2222"])

    # write_sshd_config(sshd_config_lines)

    # # Example: Get the value of a boolean setting
    # print(f"PermitRootLogin: {get_boolean_setting(sshd_config_lines, 'PermitRootLogin')}")

    # # Example: Get the list of values for a setting
    # print(f"AllowUsers: {get_list_setting(sshd_config_lines, 'AllowUsers')}")

    disable_ssh()