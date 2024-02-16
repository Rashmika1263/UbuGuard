import subprocess
import json

def get_last_activities(user='', num_entries=10):
    try:
        # Run the 'grep' command to filter auth.log entries
        result = subprocess.run(['grep', '-a' , user, '/var/log/auth.log'], stdout=subprocess.PIPE, text=True, check=True)

        # Split the output into lines
        lines = result.stdout.splitlines()

        activities = []

        for line in lines[-num_entries:]:
            # Extract relevant information (timestamp and activity details)
            month, date, time, activity_details = line.split(maxsplit=3)
            activity_data = {"timestamp": month+' '+date+' '+time, "activity": activity_details}

            activities.append(activity_data)

    except subprocess.CalledProcessError as e:
        activities = [{"error": f"Error running 'grep' command: {e}"}]

    return activities

if __name__ == "__main__":
    # Specify the number of entries you want to retrieve
    num_entries = 10

    last_activities = get_last_activities('ubuntu',num_entries)
    json_output = json.dumps(last_activities, indent=2)
    print(json_output)
