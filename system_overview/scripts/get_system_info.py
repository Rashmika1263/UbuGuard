import subprocess
import json
import os

CACHE_FILE = 'system_info_cache.json'

def run_inxi_command(command):
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode == 0:
        return result.stdout.strip()
    else:
        print(f"Error running {command[0]} command: {result.stderr}")
        return None

def get_system_info():
    # Check if the cache file exists
    if os.path.exists(CACHE_FILE):
        # Load data from the cache file
        with open(CACHE_FILE, 'r') as file:
            return json.load(file)

    # Run different inxi commands to get specific information
    system_info = {
        'cpu_info': run_inxi_command(['inxi', '-C']),
        'memory_info': run_inxi_command(['inxi', '-m']),
        'system_info': run_inxi_command(['inxi', '-S']),
        'machine_info': run_inxi_command(['inxi', '-M']),
        'disk_info': run_inxi_command(['inxi', '-D']),
        'graphics_info': run_inxi_command(['inxi', '-G']),
        'audio_info': run_inxi_command(['inxi', '-A']),
        'network_info': run_inxi_command(['inxi', '-i']),
        'partition_info': run_inxi_command(['inxi', '-p']),
        # 'disk_info': run_inxi_command(['inxi', '-D']),
        # 'disk_info': run_inxi_command(['inxi', '-D']),
        # 'disk_info': run_inxi_command(['inxi', '-D']),
        # Add more information as needed
    }

    # Update the cache file
    with open(CACHE_FILE, 'w') as file:
        json.dump(system_info, file)

    return system_info

if __name__ == "__main__":
    # If you run this script directly, print the system info
    system_info = get_system_info()
    if system_info:
        print(json.dumps(system_info, indent=4))
