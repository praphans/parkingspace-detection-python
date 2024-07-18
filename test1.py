# เรียกใช้งานไลบรารีที่จำเป็น
import cv2                   # เรียกใช้ OpenCV เพื่อทำงานกับวิดีโอและรูปภาพ
import numpy as np           # เรียกใช้ NumPy เพื่อการคำนวณทางคณิตศาสตร์และการจัดการข้อมูลที่มีโครงสร้าง
import cvzone                # เรียกใช้งาน cvzone เพื่อฟังก์ชันที่ช่วยในการวาดข้อความบนภาพ
import pickle                # เรียกใช้งาน pickle เพื่อการบันทึกและโหลดข้อมูลไฟล์

# เปิดการใช้งานวิดีโอ
cap = cv2.VideoCapture('easy.mp4')
#cap = cv2.VideoCapture('easy2.png')

# กำหนดค่าตัวแปรเริ่มต้นสำหรับการวาด
drawing = False          # ตัวแปรสำหรับตรวจสอบว่ากำลังวาดหรือไม่
area_names = []          # รายชื่อของพื้นที่ที่ถูกวาด

# โหลดข้อมูล polylines และ area_names จากไฟล์ "freedomtech" 
try:
    with open("freedomtech","rb") as f:
            data=pickle.load(f)
            polylines,area_names=data['polylines'],data['area_names']
except:
    polylines=[]

# กำหนดค่าเริ่มต้นให้กับตัวแปร
points = []              # จุดที่ถูกเลือกในขณะที่วาด
polylines = []           # รายการของพื้นที่ที่วาดไว้
current_name = " "        # ชื่อของพื้นที่ที่กำลังวาดอยู่ในขณะนั้น

# ฟังก์ชันสำหรับการวาดพื้นที่บนภาพ
def draw(event, x, y, flags, param):
    global points, drawing
    drawing = True
    if event == cv2.EVENT_LBUTTONDOWN:         # ถ้ามีการคลิกเมาส์ทางด้านซ้าย
        points = [(x, y)]                       # บันทึกจุดเริ่มต้น
    elif event == cv2.EVENT_MOUSEMOVE:          # ถ้ามีการเลื่อนเมาส์
        if drawing:
            points.append((x, y))               # เพิ่มจุดลงในรายการ
    elif event == cv2.EVENT_LBUTTONUP:          # ถ้ามีการปล่อยคลิกเมาส์
        drawing = False
        current_name = input('areaname:-')      # รับชื่อของพื้นที่จากผู้ใช้
        if current_name:                        # ถ้ามีชื่อที่ใส่เข้ามา
            area_names.append(current_name)    # เพิ่มชื่อของพื้นที่
            polylines.append(np.array(points, np.int32))  # เพิ่มพื้นที่ที่วาดไว้ในรายการ
    
    
# วนลูปเพื่อแสดงวิดีโอและทำการวาดพื้นที่
while True:
    ret, frame = cap.read()               # อ่านเฟรมจากวิดีโอ
    if not ret:                           # ถ้าไม่สามารถอ่านเฟรมได้
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # ย้อนกลับไปที่จุดเริ่มต้นของวิดีโอ
        continue
    frame = cv2.resize(frame, (1020, 500))  # ปรับขนาดเฟรมให้เหมาะสม
    for i, polyline in enumerate(polylines):
        print(i)     # พิมพ์ข้อความบอกชื่อพื้นที่และดัชนี
        cv2.polylines(frame, [polyline], True, (0, 0, 255), 2)  # วาดพื้นที่บนเฟรม
        cvzone.putTextRect(frame, f'{area_names[i]}', tuple(polyline[0]), 1, 1)  # เพิ่มข้อความบอกชื่อพื้นที่
    cv2.imshow('FRAME', frame)            # แสดงเฟรม
    cv2.setMouseCallback('FRAME', draw)   # กำหนดฟังก์ชันสำหรับการเช็คเมาส์
    Key = cv2.waitKey(100) & 0xFF         # รอการกดปุ่มจากคีย์บอร์ด
    if Key == ord('s'):                    # ถ้ากดปุ่ม 's'
        with open("freedomtech", "wb") as f:   # เปิดไฟล์ "freedomtech" เพื่อบันทึกข้อมูล
            data = {'polylines': polylines, 'area_names': area_names}
            pickle.dump(data, f)              # บันทึกข้อมูลลงในไฟล์

# ปิดการใช้งานวิดีโอและปิดหน้าต่าง
cap.release()
cv2.destroyAllWindows()
