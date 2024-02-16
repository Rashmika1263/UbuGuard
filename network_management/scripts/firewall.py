import subprocess

def check_ufw_status():
    try:
        # Run the ufw status command
        result = subprocess.run(['ufw', 'status'], capture_output=True, text=True, check=True)

        # Check the output for the firewall status
        if "Status: active" in result.stdout:
            return "Firewall is active"
        else:
            return "Firewall is inactive"
    except subprocess.CalledProcessError as e:
        return f"Error: {e.stderr}"

def enable_ufw():
    try:
        # Run the ufw enable command
        subprocess.run(['ufw', 'enable'], check=True)
        return "Firewall enabled successfully"
    except subprocess.CalledProcessError as e:
        return f"Error: {e.stderr}"

def disable_ufw():
    try:
        # Run the ufw disable command
        subprocess.run(['ufw', 'disable'], check=True)
        return "Firewall disabled successfully"
    except subprocess.CalledProcessError as e:
        return f"Error: {e.stderr}"

# Example usage:
# status = check_ufw_status()
# print(status)

# Uncomment and run the following lines to enable or disable the firewall
# enable_result = enable_ufw()
# print(enable_result)

# disable_result = disable_ufw()
# print(disable_result)
