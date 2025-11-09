import csv
import matplotlib.pyplot as plt
import datetime
from collections import defaultdict

def generate_reports(csv_file='posture_data.csv'):
    data = []
    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            row['timestamp'] = datetime.datetime.fromisoformat(row['timestamp'])
            row['neck_angle'] = float(row['neck_angle'])
            row['torso_angle'] = float(row['torso_angle'])
            row['offset'] = float(row['offset'])
            row['good_frames'] = int(row['good_frames'])
            row['bad_frames'] = int(row['bad_frames'])
            data.append(row)

    if not data:
        print("No data available for reports.")
        return

    # Group by date
    daily_data = defaultdict(list)
    for row in data:
        date = row['timestamp'].date()
        daily_data[date].append(row)

    # Calculate daily stats
    dates = []
    good_percentages = []
    bad_percentages = []
    avg_neck_angles = []
    avg_torso_angles = []

    for date, rows in sorted(daily_data.items()):
        total_frames = len(rows)
        good_count = sum(1 for r in rows if r['posture_status'] == 'good')
        bad_count = sum(1 for r in rows if r['posture_status'] == 'bad')
        good_percentage = (good_count / total_frames) * 100 if total_frames > 0 else 0
        bad_percentage = (bad_count / total_frames) * 100 if total_frames > 0 else 0
        avg_neck = sum(r['neck_angle'] for r in rows) / total_frames
        avg_torso = sum(r['torso_angle'] for r in rows) / total_frames

        dates.append(date)
        good_percentages.append(good_percentage)
        bad_percentages.append(bad_percentage)
        avg_neck_angles.append(avg_neck)
        avg_torso_angles.append(avg_torso)

    # Plot good/bad posture percentages over days
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

    ax1.plot(dates, good_percentages, label='Good Posture %', color='green')
    ax1.plot(dates, bad_percentages, label='Bad Posture %', color='red')
    ax1.set_title('Daily Posture Percentages')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Percentage')
    ax1.legend()
    ax1.grid(True)

    # Plot average angles over days
    ax2.plot(dates, avg_neck_angles, label='Avg Neck Angle', color='blue')
    ax2.plot(dates, avg_torso_angles, label='Avg Torso Angle', color='orange')
    ax2.set_title('Average Angles Over Days')
    ax2.set_xlabel('Date')
    ax2.set_ylabel('Angle (degrees)')
    ax2.legend()
    ax2.grid(True)

    plt.tight_layout()
    plt.savefig('posture_report.png')
    plt.show()

if __name__ == "__main__":
    generate_reports()
