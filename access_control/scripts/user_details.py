import subprocess
import json

def get_user_details(username):
    try:
        # Run the 'id' command with the specified username
        result = subprocess.run(["id", username], capture_output=True, text=True, check=True)

        # Parse the output and convert it to a dictionary
        user_details = {}
        for item in result.stdout.strip().split():
            key, value = item.split("=")
            user_details[key] = value

        # Convert the dictionary to JSON and print it
        json_output = json.dumps(user_details, indent=2)
        print(json_output)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Get the username from the user
    username = input("Enter username: ")

    # Call the function to get user details
    get_user_details(username)
