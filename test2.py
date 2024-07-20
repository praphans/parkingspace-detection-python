# Import necessary libraries
import cv2                   # Import OpenCV for video and image processing
import numpy as np           # Import NumPy for mathematical calculations and data manipulation
import pickle                # Import pickle for saving and loading data files
import pandas as pd          # Import pandas for table-like data management
from ultralytics import YOLO  # Import YOLO from the ultralytics library
import cvzone                # Import cvzone for functions to draw text on images

# Load polylines and area_names from "freedomtech" file
with open("freedomtech", "rb") as f:
    data = pickle.load(f)
    polylines, area_names = data['polylines'], data['area_names']

# Read "coco.txt" file and split data into a list of classes
with open("coco.txt", "r") as my_file:
    data = my_file.read()
class_list = data.split("\n")

# Load YOLO model
model = YOLO('yolov8s.pt')

# Open video capture
cap = cv2.VideoCapture('easy1.mp4')

count = 0  # Frame counter

# Loop to read frames and process them
while True:
    ret, frame = cap.read()  # Read frame from video
    if not ret:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Reset to the start of the video when finished
        continue

    count += 1
    if count % 3 != 0:  # Process frames at a reduced rate
        continue

    frame = cv2.resize(frame, (1020, 500))  # Resize frame for consistency

    # Predict results with YOLO
    results = model.predict(frame)
    a = results[0].boxes.data
    px = pd.DataFrame(a).astype("float")
    list1 = []

    # Process object positions
    for index, row in px.iterrows():
        x1 = int(row[0])
        y1 = int(row[1])
        x2 = int(row[2])
        y2 = int(row[3])
        d = int(row[5])
        c = class_list[d]
        cx = int(x1 + x2) // 2
        cy = int(y1 + y2) // 2
        if 'car' in c:
            list1.append([cx, cy])
            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 255, 255), 2)  # White rectangle for detected cars

    counter1 = []  # Variable to store counted cars

    # Draw areas and check parking
    for i, polyline in enumerate(polylines):
        print(i)  # Log area name and index
        cv2.polylines(frame, [polyline], True, (0, 255, 0), 2)  # Green frame for empty parking areas
        cvzone.putTextRect(frame, f'{area_names[i]}', tuple(polyline[0]), 1, 1)  # Add text for area name
        for i1 in list1:
            cx1 = i1[0]
            cy1 = i1[1]
            result = cv2.pointPolygonTest(polyline, (cx1, cy1), False)
            if result >= 0:
                cv2.circle(frame, (cx1, cy1), 5, (255, 0, 0), -1)  # Blue dot to mark car position
                cv2.polylines(frame, [polyline], True, (0, 0, 255), 2)  # Red frame when car is in the area
                counter1.append(cx1)  # Count parked cars

    # Calculate car count and free spaces
    car_count = len(counter1)  # Number of parked cars
    free_space = len(polylines) - car_count  # Number of free spaces

    # Add result text to the frame
    cvzone.putTextRect(frame, f'CAR COUNTER: {car_count}', (50, 60), 2, 2)  # Display number of parked cars
    cvzone.putTextRect(frame, f'CAR FREE SPACE: {free_space}', (50, 110), 2, 2)  # Display number of free spaces

    # Show frame
    cv2.imshow('FRAME', frame)
    key = cv2.waitKey(1) & 0xFF

# Release video capture and close windows
cap.release()
cv2.destroyAllWindows()
