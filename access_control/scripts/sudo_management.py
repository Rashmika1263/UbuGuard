import subprocess

def add_user_to_sudo(username):
    try:
        subprocess.run(['sudo', 'usermod', '-aG', 'sudo', username], check=True)
        print(f"User '{username}' added to the sudo group successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error adding user '{username}' to the sudo group: {e}")

def remove_user_from_sudo(username):
    try:
        subprocess.run(['sudo', 'deluser', username, 'sudo'], check=True)
        print(f"User '{username}' removed from the sudo group successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error removing user '{username}' from the sudo group: {e}")

def list_sudo_users():
    sudo_data = []
    try:
        result = subprocess.run(['getent', 'group', 'sudo'], stdout=subprocess.PIPE, check=True)
        sudo_users = result.stdout.decode('utf-8').split(':')[3].split(',')
        for user in sudo_users:
            sudo_data.append(user)
        return sudo_data
    except subprocess.CalledProcessError as e:
        print(f"Error listing sudo users: {e}")

# Example Usage
# Uncomment and modify the following lines as needed
# add_user_to_sudo('newuser')
# remove_user_from_sudo('existinguser')
# print(list_sudo_users())

