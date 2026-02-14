from flask import Flask, render_template, request, redirect
from datetime import datetime
import os

app = Flask(__name__)

CSV_FILE = 'data/log.csv'
os.makedirs("data", exist_ok=True)

def add_activity_csv(name: str):
    date_of_activity = datetime.now().strftime("%Y-%m-%d %H:%M")
    status = 'active'
    with open(CSV_FILE, 'a') as file:
        file.write(f"{name},{date_of_activity},{status}\n")

def stop_activity_csv(name: str):
    try:
        with open(CSV_FILE, 'r') as file:
            lines = file.readlines()
        updated_lines = []
        for line in lines:
            parts = line.strip().split(',')
            if len(parts) >= 3 and parts[0] == name and parts[2] == 'active':
                date_of_stop = datetime.now().strftime("%Y-%m-%d %H:%M")
                updated_lines.append(f"{parts[0]},{parts[1]},stopped,{date_of_stop}\n")
            else:
                updated_lines.append(line)
        with open(CSV_FILE, 'w') as file:
            file.writelines(updated_lines)
    except FileNotFoundError:
        pass

def get_activities():
    activities = []
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, 'r') as file:
            for line in file:
                parts = line.strip().split(',')
                activities.append(parts)
    return activities

def calculate_time_spent(name: str):
    activities = get_activities()
    for act in activities:
        if len(act) == 4 and act[0] == name and act[2] == 'stopped':
            start = datetime.strptime(act[1], "%Y-%m-%d %H:%M")
            stop = datetime.strptime(act[3], "%Y-%m-%d %H:%M")
            diff = stop - start
            if diff.days < 1:
                if diff.seconds < 3600:
                    return f"{diff.seconds // 60} minutes"
                else:
                    return f"{diff.seconds // 3600} hours and {(diff.seconds % 3600) // 60} minutes"
            else:
                return f"{diff.days} days, {diff.seconds // 3600} hours and {(diff.seconds % 3600) // 60} minutes"
    return None

@app.route("/")
def home():
    activities = get_activities()
    return render_template("index.html", activities=activities)

@app.route("/add", methods=["POST"])
def add_activity():
    name = request.form["name"]
    add_activity_csv(name)
    return redirect("/")

@app.route("/stop/<activity_name>")
def stop_activity(activity_name):
    stop_activity_csv(activity_name)
    return redirect("/")

@app.route("/time/<activity_name>")
def time_spent(activity_name):
    spent = calculate_time_spent(activity_name)
    return render_template("time.html", activity=activity_name, spent=spent)

if __name__ == "__main__":
    app.run(debug=True)
