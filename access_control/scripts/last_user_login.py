import subprocess
import json

def get_last_login_users():
    users_data = []

    try:
        # Run the 'last' command and capture its output
        result = subprocess.run(['last'], stdout=subprocess.PIPE, text=True, check=True)

        # Split the output into lines
        lines = result.stdout.splitlines()

        # Extract information about the last login users
        for line in lines[-15:]:
            if line.strip():  # Skip empty lines
                # Split the line into fields
                fields = line.split()

                # Extract relevant information (username and login time)
                username = fields[0]

                # Check for the "still" case
                if fields[-1] == 'still':
                    user_data = {"user": username, "last_login": "Currently logged in"}
                else:
                    # Extract the time from the text itself
                    login_time_str = ' '.join(fields[7:])
                    user_data = {"user": username, "last_login": login_time_str}

                users_data.append(user_data)

    except subprocess.CalledProcessError as e:
        print(f"Error running 'last' command: {e}")

    return users_data

if __name__ == "__main__":
    last_login_users = get_last_login_users()
    json_output = json.dumps(last_login_users, indent=2)
    print(json_output)
