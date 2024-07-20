# Import necessary libraries
import cv2                   # Import OpenCV for video and image processing
import numpy as np           # Import NumPy for mathematical calculations and data manipulation
import cvzone                # Import cvzone for functions to draw text on images
import pickle                # Import pickle for saving and loading data files

# Open video capture
cap = cv2.VideoCapture('easy1.mp4')
#cap = cv2.VideoCapture('easy2.png')

# Set default variables for drawing
drawing = False          # Variable to check if drawing is in progress
area_names = []          # List of names of areas being drawn

# Load polylines and area_names from "freedomtech" file
try:
    with open("freedomtech", "rb") as f:
        data = pickle.load(f)
        polylines, area_names = data['polylines'], data['area_names']
except:
    polylines = []

# Initialize variables
points = []              # Points selected while drawing
polylines = []           # List of drawn areas
current_name = " "        # Name of the area being drawn

# Function to draw areas on the image
def draw(event, x, y, flags, param):
    global points, drawing
    drawing = True
    if event == cv2.EVENT_LBUTTONDOWN:         # If left mouse button is clicked
        points = [(x, y)]                       # Save starting point
    elif event == cv2.EVENT_MOUSEMOVE:          # If mouse is moved
        if drawing:
            points.append((x, y))               # Add point to the list
    elif event == cv2.EVENT_LBUTTONUP:          # If left mouse button is released
        drawing = False
        current_name = input('areaname:-')      # Get area name from user
        if current_name:                        # If a name is provided
            area_names.append(current_name)    # Add area name
            polylines.append(np.array(points, np.int32))  # Add drawn area to the list

# Loop to display video and draw areas
while True:
    ret, frame = cap.read()               # Read frame from video
    if not ret:                           # If frame cannot be read
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Go back to the start of the video
        continue
    frame = cv2.resize(frame, (1020, 500))  # Resize frame to suitable dimensions
    for i, polyline in enumerate(polylines):
        print(i)     # Print area name and index
        cv2.polylines(frame, [polyline], True, (0, 0, 255), 2)  # Draw area on frame
        cvzone.putTextRect(frame, f'{area_names[i]}', tuple(polyline[0]), 1, 1)  # Add area name text
    cv2.imshow('FRAME', frame)            # Display frame
    cv2.setMouseCallback('FRAME', draw)   # Set mouse callback function
    Key = cv2.waitKey(100) & 0xFF         # Wait for key press
    if Key == ord('s'):                    # If 's' key is pressed
        with open("freedomtech", "wb") as f:   # Open "freedomtech" file to save data
            data = {'polylines': polylines, 'area_names': area_names}
            pickle.dump(data, f)              # Save data to file

# Release video capture and close windows
cap.release()
cv2.destroyAllWindows()
