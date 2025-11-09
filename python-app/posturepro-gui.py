import cv2
import time
import math as m
import mediapipe as mp
import csv
import datetime

def findDistance(x1, y1, x2, y2):
    return m.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def findAngle(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    denominator = m.sqrt(dx**2 + dy**2) * abs(y1)
    numerator = dy * (-y1)
    if denominator == 0:
        return 0
    cos_theta = numerator / denominator
    cos_theta = min(1, max(-1, cos_theta))
    theta = m.acos(cos_theta)
    degree = theta * (180 / m.pi)
    return degree

def sendWarning():
    print("Warning: Bad posture detected for too long!")

good_frames = 0
bad_frames = 0
font = cv2.FONT_HERSHEY_SIMPLEX

csv_file = open('posture_data.csv', 'a', newline='')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['timestamp', 'neck_angle', 'torso_angle', 'offset', 'pose_status', 'good_frames', 'bad_frames'])

blue = (255, 127, 0)
red = (50, 50, 255)
green = (0, 255, 0)
light_green = (127, 233, 100)
yellow = (0, 255, 255)

mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils
drawing_spec_good = mp_drawing.DrawingSpec(color=(0,255,0), thickness=4, circle_radius=4)
drawing_spec_bad = mp_drawing.DrawingSpec(color=(0,0,255), thickness=4, circle_radius=4)
suggestion_text = ""

if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open video.")
        exit()

    fps = int(cap.get(cv2.CAP_PROP_FPS))
    if fps == 0:
        fps = 30

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_size = (width, height)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_output = cv2.VideoWriter('output.mp4', fourcc, fps, frame_size)
    total_frames = 0

    # Adjust these after seeing your live output!
    GOOD_NECK = 50   # Set to your "good" posture neck value plus a little margin
    GOOD_TORSO = 15  # Set to your "good" posture torso value plus margin
    GOOD_OFFSET = 400  # Set to your observed "good posture" shoulder offset + margin

    while True:
        success, image = cap.read()
        if not success:
            print("Skipping empty frame.")
            continue

        total_frames += 1
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        keypoints = pose.process(image_rgb)

        if not keypoints.pose_landmarks:
            cv2.putText(image, "No pose detected", (10, 30), font, 0.9, red, 2)
            cv2.imshow('MediaPipe Pose', image)
            if cv2.waitKey(5) & 0xFF == ord('q'):
                break
            continue

        lm = keypoints.pose_landmarks
        lmPose = mp_pose.PoseLandmark
        h, w = image.shape[:2]

        try:
            l_shldr_x = int(lm.landmark[lmPose.LEFT_SHOULDER].x * w)
            l_shldr_y = int(lm.landmark[lmPose.LEFT_SHOULDER].y * h)
            r_shldr_x = int(lm.landmark[lmPose.RIGHT_SHOULDER].x * w)
            r_shldr_y = int(lm.landmark[lmPose.RIGHT_SHOULDER].y * h)
            l_ear_x = int(lm.landmark[lmPose.LEFT_EAR].x * w)
            l_ear_y = int(lm.landmark[lmPose.LEFT_EAR].y * h)
            l_hip_x = int(lm.landmark[lmPose.LEFT_HIP].x * w)
            l_hip_y = int(lm.landmark[lmPose.LEFT_HIP].y * h)

            offset = findDistance(l_shldr_x, l_shldr_y, r_shldr_x, r_shldr_y)
            neck_inclination = findAngle(l_shldr_x, l_shldr_y, l_ear_x, l_ear_y)
            torso_inclination = findAngle(l_hip_x, l_hip_y, l_shldr_x, l_shldr_y)

            # Print the current calibration for your live posture
            print(f"Neck: {neck_inclination:.1f}, Torso: {torso_inclination:.1f}, Offset: {offset:.1f}")

            # Dynamic threshold text/colors
            if offset < GOOD_OFFSET:
                offset_text = 'Aligned'
                offset_color = green
            else:
                offset_text = 'Not Aligned'
                offset_color = red

            angle_text_string = f'Neck: {int(neck_inclination)}  Torso: {int(torso_inclination)}'

            # Posture logic
            if neck_inclination < GOOD_NECK and torso_inclination < GOOD_TORSO and offset < GOOD_OFFSET:
                bad_frames = 0
                good_frames += 1
                color = light_green
                pose_status = 'good'
                suggestion_text = ""
            else:
                good_frames = 0
                bad_frames += 1
                color = red
                pose_status = 'bad'
                # Suggestion
                if neck_inclination >= GOOD_NECK:
                    suggestion_text = "Sit straight, keep your head facing forward."
                elif torso_inclination >= GOOD_TORSO:
                    suggestion_text = "Keep your torso upright."
                elif offset >= GOOD_OFFSET:
                    suggestion_text = "Align your shoulders."
                if bad_frames > fps * 5:
                    sendWarning()

            # Log data to CSV
            timestamp = datetime.datetime.now().isoformat()
            csv_writer.writerow([timestamp, neck_inclination, torso_inclination, offset, pose_status, good_frames, bad_frames])

            cv2.putText(image, offset_text + f' ({int(offset)})', (w - 220, 30), font, 0.9, offset_color, 2)
            cv2.putText(image, angle_text_string, (10, 30), font, 0.9, color, 2)

            good_time = (1 / fps) * good_frames if fps > 0 else 0
            bad_time = (1 / fps) * bad_frames if fps > 0 else 0

            if good_time > 0:
                cv2.putText(image, f'Good Posture Time: {round(good_time,1)}s', (10, h - 80), font, 0.9, green, 2)
            else:
                cv2.putText(image, f'Bad Posture Time: {round(bad_time,1)}s', (10, h - 80), font, 0.9, red, 2)

            posture_score = (good_frames / total_frames) * 100 if total_frames > 0 else 0
            score_text = f'Posture Score: {posture_score:.1f}%'
            cv2.putText(image, score_text, (10, h - 50), font, 0.8, blue, 2)

            if suggestion_text:
                cv2.putText(image, suggestion_text, (10, h - 110), font, 0.8, red, 2)

            if pose_status == 'good':
                mp_drawing.draw_landmarks(image, lm, mp_pose.POSE_CONNECTIONS, drawing_spec_good, drawing_spec_good)
            else:
                mp_drawing.draw_landmarks(image, lm, mp_pose.POSE_CONNECTIONS, drawing_spec_bad, drawing_spec_bad)

        except Exception as e:
            print(f"Error: {e}")

        video_output.write(image)
        cv2.imshow('MediaPipe Pose', image)
        if cv2.waitKey(5) & 0xFF == ord('q'):
            break

    cap.release()
    video_output.release()
    cv2.destroyAllWindows()
    csv_file.close()
