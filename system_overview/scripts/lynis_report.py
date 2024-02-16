import json
import subprocess

def run_lynis_audit():
    result = subprocess.run(["lynis", "audit", "system","--no-colors"], capture_output=True, text=True)
    return result.stdout

def run_lynis_and_save_output(output_file):
    result = subprocess.run(["sudo", "lynis", "audit", "system","--no-colors"], capture_output=True, text=True)
    
    with open(output_file, 'w') as file:
        file.write(result.stdout)

def parse_lynis_output(lynis_output):
    result = {}
    current_section = None
    current_subsection = None

    for line in lynis_output:
        if line.startswith('[+] '):
            current_section = line[4:].strip()
            result[current_section] = {}
        elif current_section:
            subsection_match = line.split('[')
            if len(subsection_match) >= 3:
                current_subsection = subsection_match[1].split(']')[0].rstrip("\u001b")[2:].strip("- ")
                value = subsection_match[-1].split(']')[0].strip()
                result[current_section][current_subsection] = value

    return result

if __name__ == "__main__":
    output_file = 'lynis_output.txt'

    run_lynis_and_save_output(output_file)

    with open(output_file, 'r') as file:
        lynis_output = file.readlines()

    parsed_data = parse_lynis_output(lynis_output)
    
    json_output = json.dumps(parsed_data, indent=2)
    
    with open('output.json', 'w') as json_file:
        json_file.write(json_output)
