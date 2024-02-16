import subprocess
import crypt

def create_user(username, password):
    try:
        password_hash = crypt.crypt(password)
        subprocess.run(['sudo', 'useradd', '-m', '-p', password_hash, username], check=True)
        print(f"User '{username}' created successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error creating user '{username}': {e}")

def delete_user(username):
    try:
        subprocess.run(['sudo', 'userdel', '-r', username], check=True)
        print(f"User '{username}' deleted successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error deleting user '{username}': {e}")

def get_system_uid_range():
    try:
        with open('/etc/login.defs', 'r') as file:
            for line in file:
                if line.startswith("UID_MIN"):
                    return line.split()[1]
    except FileNotFoundError:
        print("Error: /etc/login.defs file not found.")
    except Exception as e:
        print(f"Error getting system UID range: {e}")

def list_users():
    user_details = []
    try:
        system_uid_range = get_system_uid_range()

        if system_uid_range:
            result = subprocess.run(['awk', '-F:', f'$3 >= {system_uid_range} && $3 != 65534', '/etc/passwd'], stdout=subprocess.PIPE, check=True)
            users = result.stdout.decode('utf-8').split('\n')[:-1]


            for i in range(len(users)):
                user_details.append(users[i].split(":")[0])
        return user_details
    except subprocess.CalledProcessError as e:
        print(f"Error listing users: {e}")

# Example Usage
# Uncomment and modify the following lines as needed
# create_user('newuser', 'password123')
# delete_user('newuser')
# print(list_users())