import subprocess
import json

def get_last_activities(log_dir, num_entries=20):
    try:
        # Run the 'grep' command to filter auth.log entries
        result = subprocess.run(['cat', log_dir], stdout=subprocess.PIPE, text=True, check=True)

        # Split the output into lines
        lines = result.stdout.splitlines()

        activities = []

        for line in lines[-num_entries:]:
            # Extract relevant information (timestamp and activity details)
            month, date, time, activity_details = line.split(maxsplit=3)
            host = activity_details.split(":")
            activity_data = {"timestamp": month+' '+date+' '+time,"host":host[0] ,"activity": host[1][1:]}

            activities.append(activity_data)

    except subprocess.CalledProcessError as e:
        activities = [{"error": f"Error running 'grep' command: {e}"}]

    return activities

if __name__ == "__main__":
    # Specify the number of entries you want to retrieve
    num_entries = 5

    last_activities = get_last_activities(log_dir='/var/log/syslog',num_entries=num_entries)
    json_output = json.dumps(last_activities, indent=2)
    print(json_output)
