from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import csv
import os

app = Flask(__name__)
CSV_FILE = 'data/log.csv'

def read_activities():
    activities = []
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, 'r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                activities.append(row)
    return activities

def write_activities(activities):
    with open(CSV_FILE, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(activities)

def calculate_time(start_str, stop_str):
    start = datetime.strptime(start_str, "%Y-%m-%d %H:%M")
    stop = datetime.strptime(stop_str, "%Y-%m-%d %H:%M")
    diff = stop - start
    if diff.days < 1:
        hours = diff.seconds // 3600
        minutes = (diff.seconds % 3600) // 60
        if hours > 0:
            return f"{hours}h {minutes}m"
        else:
            return f"{minutes}m"
    else:
        hours = diff.seconds // 3600
        minutes = (diff.seconds % 3600) // 60
        return f"{diff.days}d {hours}h {minutes}m"

def get_statistics(activities):
    active_count = sum(1 for act in activities if act[2] == 'active')
    stopped_count = sum(1 for act in activities if act[2] == 'stopped')
    total_times = []
    for act in activities:
        if act[2] == 'stopped':
            start = datetime.strptime(act[1], "%Y-%m-%d %H:%M")
            stop = datetime.strptime(act[3], "%Y-%m-%d %H:%M")
            total_times.append((stop - start).total_seconds())
    avg_time = None
    if total_times:
        avg_seconds = sum(total_times)/len(total_times)
        hours = int(avg_seconds // 3600)
        minutes = int((avg_seconds % 3600) // 60)
        avg_time = f"{hours}h {minutes}m"
    return active_count, stopped_count, avg_time

@app.route('/')
def index():
    activities = read_activities()
    activities.sort(key=lambda x: x[1])  # sort by start date

    # Dodajemy czas spędzony dla zakończonych aktywności
    display_activities = []
    for act in activities:
        display_act = act.copy()
        if act[2] == 'stopped' and act[3]:
            display_act.append(calculate_time(act[1], act[3]))  # dodajemy 5. element = czas
        else:
            display_act.append(None)  # dla aktywnych brak czasu
        display_activities.append(display_act)

    active_count, stopped_count, avg_time = get_statistics(activities)
    return render_template(
        'index.html',
        activities=display_activities,
        active_count=active_count,
        stopped_count=stopped_count,
        avg_time=avg_time
    )


@app.route('/add', methods=['POST'])
def add_activity():
    name = request.form['name']
    date_of_start = datetime.now().strftime("%Y-%m-%d %H:%M")
    activities = read_activities()
    activities.append([name, date_of_start, 'active', ''])
    write_activities(activities)
    return redirect(url_for('index'))

@app.route('/stop/<name>')
def stop_activity(name):
    activities = read_activities()
    for i, act in enumerate(activities):
        if act[0] == name and act[2] == 'active':
            activities[i][2] = 'stopped'
            activities[i][3] = datetime.now().strftime("%Y-%m-%d %H:%M")
            break
    write_activities(activities)
    return redirect(url_for('index'))

if __name__ == '__main__':
    os.makedirs('data', exist_ok=True)
    if not os.path.exists(CSV_FILE):
        open(CSV_FILE, 'w').close()
    app.run(debug=True)