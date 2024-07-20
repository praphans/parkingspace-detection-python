## Parkingspace-Detection

### Overview

This project utilizes YOLOv8s with Python to detect empty parking spaces and count the number of cars in a parking lot. It consists of two main scripts:

- **test1.py**: This script is used to draw lines for the parking spaces.
- **test2.py**: This script counts the number of parking spaces and cars.

### Required Libraries

To run this project, you need to install the following libraries:

- **cv2**: OpenCV library for computer vision tasks.
- **numpy**: Fundamental package for scientific computing with Python.
- **cvzone**: Computer vision package to make tasks easier.
- **pickle**: Python library for serializing and deserializing objects.
- **pandas**: Data manipulation and analysis library.
- **ultralytics**: YOLOv8 implementation for object detection.

### Recommended Software

In the `software` folder, you will find recommended software tools to enhance your workflow and usage of this project.

### Getting Started

1. Clone the repository.
2. Install the required libraries using pip:
   ```sh
   pip install cv2 numpy cvzone pickle pandas ultralytics
   ```
3. Run `test1.py` to draw lines for the parking spaces.
4. Run `test2.py` to count the number of parking spaces and cars.

### Usage

- **test1.py**: Execute this script to mark and define parking spaces in your input video or image.
- **test2.py**: Execute this script to detect and count empty parking spaces and cars using the defined parking spaces.

# Demo Screenshots
![alt text](https://github.com/praphanth/parkingspace-detection-python/img-demo.png?raw=true)