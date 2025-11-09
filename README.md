# Ergonomic Office Chair: Real-Time Posture Detection System

It is a real-time posture detection tool designed to help users maintain healthy posture by identifying and alerting them to poor posture. Our system offers both a Python GUI application and a web-based solution to cater to different user preferences.


## Project Overview
A smart chair posture detection system for monitoring, logging, and improving sitting posture. Logs collected data for every frame in CSV files, analyzed via machine learning for ergonomic risk. Offers real-time feedback, tracking, reports, and notifications to promote better workplace ergonomics.
## Purpose
- Detect poor posture among users in real-time.
- Provide instant feedback to promote healthier sitting habits.
## Key Features
- Real-time posture analysis and alerts
- Visual feedback indicating good or poor posture
- Tracking of neck and torso angles for detailed posture assessment
- Available in both desktop and web formats
## Tech Stack
### Frontend
- HTML, CSS, JavaScript for user interface and real-time visualization
### Backend
- Python for data processing, posture analysis, and report generation
### Computer Vision & Pose Detection
- OpenCV and MediaPipe for real-time frame processing and extraction of body keypoints
### Machine Learning Algorithms
- Multiple Linear Regression (MLR) for modeling posture-angle relationships
- Random Forest classifier for posture category prediction
### Data Handling
- CSV files for datalogging every frame, used for feedback and analytics


## Applications
The project contains two main applications:

1. **Python GUI Application** (`/python-app`)

   - Desktop-based solution using OpenCV and MediaPipe
   - Direct webcam integration
   - Low-latency processing
   - [Setup Instructions](./python-app/README.md)

2. **Web Application** (`/web-app`)
   - Browser-based solution using MediaPipe
   - No installation required
   - Cross-platform compatibility
   - [Setup Instructions](./docs/README.md)

## How It Works

- **Body Tracking**: Utilizes advanced computer vision to detect key body points like shoulders, neck, and hips
- **Posture Analysis**: Calculates metrics such as shoulder width and neck and torso angles
- **Feedback**: Real-time alerts are displayed for poor posture, with colors indicating alignment status. Data analytics and prediction done to predict the upcoming posture using ml algorithms
- 
=======
# ErgonomicOfficeChair
A smart chair posture detection system for monitoring, logging, and improving sitting posture. Logs collected data for every frame in CSV files, analyzed via machine learning for ergonomic risk. Offers real-time feedback, tracking, reports, and notifications to promote better workplace ergonomics

