from datetime import datetime

CSV_FILE = 'data/log.csv'

def add_activity():
    new_activity = input("Enter the name of the activity:\n")
    date_of_activity = datetime.now().strftime("%Y-%m-%d %H:%M")
    status = 'active'
    with open(CSV_FILE, 'a') as file:
        file.write(f"{new_activity},{date_of_activity},{status}\n")
    print("Activity added successfully.")

def view_active_activities():
    try:
        with open(CSV_FILE, 'r') as file:
            lines = file.readlines()
            active = [line.strip() for line in lines if line.strip().split(',')[2] == 'active']
            if active:
                for act in active:
                    name, date, status = act.split(',')
                    print(f"Activity: {name}, Started at: {date}")
            else:
                print("No active activities found.")
    except FileNotFoundError:
        print("No activities yet.")

def stop_activity():
    activity_to_stop = input("Enter the name of the activity to stop:\n")
    try:
        with open(CSV_FILE, 'r') as file:
            lines = file.readlines()
        updated_lines = []
        found = False
        for line in lines:
            name, date, status = line.strip().split(',')
            if name == activity_to_stop and status == 'active':
                date_of_stop = datetime.now().strftime("%Y-%m-%d %H:%M")
                updated_lines.append(f"{name},{date},stopped,{date_of_stop}\n")
                found = True
            else:
                updated_lines.append(line)
        with open(CSV_FILE, 'w') as file:
            file.writelines(updated_lines)
        if found:
            print(f'Activity "{activity_to_stop}" stopped successfully.')
        else:
            print(f'Activity "{activity_to_stop}" not found or already stopped.')
    except FileNotFoundError:
        print("No activities yet.")

def view_stopped_activities():
    try:
        with open(CSV_FILE, 'r') as file:
            lines = file.readlines()
            stopped = [line.strip() for line in lines if line.strip().split(',')[2] == 'stopped']
            if stopped:
                for stop in stopped:
                    name, date, status, date_of_stop = stop.split(',')
                    print(f"Activity: {name}, Started at: {date}, Stopped at: {date_of_stop}")
            else:
                print("No stopped activities found.")
    except FileNotFoundError:
        print("No activities yet.")
        
def time_spent() -> None:
    try:
        with open(CSV_FILE, 'r') as file:
            lines = file.readlines()
            activity = str(input('Enter the name of the activity:\n'))
            for line in lines:   
                name, date, status, date_of_stop = line.strip().split(',')
                if name == activity and status == 'stopped':
                    start = datetime.strptime(date, "%Y-%m-%d %H:%M")
                    stop = datetime.strptime(date_of_stop, "%Y-%m-%d %H:%M")
                    time_diff = stop - start
                    if time_diff.days < 1:
                        if time_diff.seconds < 3600:
                            time_diff = f"{time_diff.seconds // 60} minutes"
                        else:
                            time_diff = f'{time_diff.seconds // 3600} hours and {(time_diff.seconds % 3600) // 60} minutes '
                    else:
                        time_diff = f'{time_diff.days} days, {time_diff.seconds // 3600} hours and {(time_diff.seconds % 3600) // 60} minutes'
                    print(f'Time spent on {activity}: {time_diff}')
                else:
                    print(f'Activity "{activity}" not found or not stopped yet.')
    except FileNotFoundError:
        print("No activities yet.")                    

def main():
    while True:
        print("\nChoose an option:")
        print("1. Add a new activity")
        print("2. View active activities")
        print("3. Stop an activity")
        print("4. View stopped activities")
        print("5. View time spent on an activity")
        print("6. End the program")
        choice = input(": ")
        match choice:
            case "1":
                add_activity()
            case "2":
                view_active_activities()
            case "3":
                stop_activity()
            case "4":
                view_stopped_activities()
            case "5":
                time_spent()
            case "6":
                print("Goodbye!")
                break
            case _:
                print("Invalid option, try again.")

if __name__ == "__main__":
    main()