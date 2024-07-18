# เรียกใช้งานไลบรารีที่จำเป็น
import cv2                   # เรียกใช้ OpenCV เพื่อทำงานกับวิดีโอและรูปภาพ
import numpy as np           # เรียกใช้ NumPy เพื่อการคำนวณทางคณิตศาสตร์และการจัดการข้อมูลที่มีโครงสร้าง
import pickle                # เรียกใช้งาน pickle เพื่อการบันทึกและโหลดข้อมูลไฟล์
import pandas as pd          # เรียกใช้งาน pandas เพื่อการจัดการข้อมูลในรูปแบบตาราง
from ultralytics import YOLO  # เรียกใช้งาน YOLO จากไลบรารี ultralytics
import cvzone                # เรียกใช้งาน cvzone เพื่อฟังก์ชันที่ช่วยในการวาดข้อความบนภาพ

# โหลดข้อมูล polylines และ area_names จากไฟล์ "freedomtech"
with open("freedomtech", "rb") as f:
    data = pickle.load(f)
    polylines, area_names = data['polylines'], data['area_names']

# อ่านไฟล์ "coco.txt" และแบ่งข้อมูลออกเป็นรายการของคลาส
my_file = open("coco.txt", "r")
data = my_file.read()
class_list = data.split("\n")

# โหลดโมเดล YOLO
model = YOLO('yolov8s.pt')

# เปิดการใช้งานวิดีโอ
cap = cv2.VideoCapture('easy.mp4')

count = 0  # ตัวแปรนับเฟรม

# วนลูปเพื่ออ่านเฟรมและประมวลผล
while True:
    ret, frame = cap.read()  # อ่านเฟรมจากวิดีโอ
    if not ret:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # ย้อนกลับไปที่จุดเริ่มต้นของวิดีโอเมื่อจบ
        continue

    count += 1
    if count % 3 != 0:  # นับเฟรมแบบเล่นสัดส่วน
        continue

    frame = cv2.resize(frame, (1020, 500))  # ปรับขนาดเฟรมให้เหมาะสม

    # ทำนายผลลัพธ์ด้วย YOLO
    results = model.predict(frame)
    a = results[0].boxes.data
    px = pd.DataFrame(a).astype("float")
    list1 = []

    # วนลูปเพื่อประมวลผลตำแหน่งของวัตถุ
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
            cv2.rectangle(frame,(x1,y1),(x2,y2),(255,255,255),2) #กรอบสีขาวตรวจจับระบุรถ
    counter1 = []  # ตัวแปรเก็บจำนวนรถ

    # วนลูปเพื่อวาดพื้นที่และตรวจสอบการจอดรถ
    for i, polyline in enumerate(polylines):
        print(i)  # พิมพ์ข้อความบอกชื่อพื้นที่และดัชนี log
        cv2.polylines(frame, [polyline], True, (0, 255, 0), 2)  # เฟรมสีเขียว รถว่าง
        cvzone.putTextRect(frame, f'{area_names[i]}', tuple(polyline[0]), 1, 1)  # เพิ่มข้อความบอกชื่อพื้นที่ log
        for i1 in list1:
            cx1 = i1[0]
            cy1 = i1[1]
            result = cv2.pointPolygonTest(polyline, ((cx1, cy1)), False)
            if result >= 0:
                cv2.circle(frame, (cx1, cy1), 5, (255, 0, 0), -1) #จุดสีน้ำเงิน Mark ตัวรถ
                cv2.polylines(frame, [polyline], True, (0, 0, 255), 2) # เปลี่ยนเฟรมสีแดง เมื่อจุดน้ำเงินเข้ามาในเฟรม
                counter1.append(cx1) #นับจำนวนรถที่จอด

    # คำนวณจำนวนรถและพื้นที่ที่ว่าง
    car_count = len(counter1) #จำนวนรถที่จอด
    free_space = len(polylines) - car_count #จำนวนที่ว่าง

    # เพิ่มข้อความแสดงผลลงบนเฟรม
    cvzone.putTextRect(frame, f'CAR COUNTER: {car_count}', (50, 60), 2, 2)  # ป้ายแสดงจำนวนรถจอด
    cvzone.putTextRect(frame, f'CAR FREE SPACE: {free_space}', (50, 110), 2, 2)  # ป้ายแสดงจำนวนที่ว่าง

    # แสดงเฟรม
    cv2.imshow('FRAME', frame)
    key = cv2.waitKey(1) & 0xFF

# ปิดการใช้งานวิดีโอและหน้าต่าง
cap.release()
cv2.destroyAllWindows()
