import ultralytics
from ultralytics import YOLO
import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import torch
import os
import sqlite3
import easyocr as ocr

# YOLO model ve OCR motorunu yükle
ultralytics.checks()
model = YOLO('runs/detect/train6/weights/best.pt')
ocr_motor = ocr.Reader(['en', 'tr'])

# Veritabanı adı
db_name = 'database/plate_database1.db'

# Video dosyasını işle
video_path = 'test_data/Car_Traffic_short1.mp4'
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("Video dosyası yüklenemedi.")
else:
    print("Video dosyası yüklendi.")

# Veritabanını oluştur
def create_database(db_name):
    if not os.path.exists(db_name):
        conn = sqlite3.connect(db_name)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS plakalar (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                Plate TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()
        print(f"Veritabanı '{db_name}' oluşturuldu.")
    else:
        print(f"Veritabanı '{db_name}' zaten mevcut.")

create_database(db_name)

# OCR ile metin tespiti ve veritabanına kaydetme
def perform_ocr_and_save(cropped_img, db_name, ocr_motor):
    cropped_img_np = np.array(cropped_img)
    cropped_img_cv2 = cv2.cvtColor(cropped_img_np, cv2.COLOR_RGB2BGR)
    plate = ocr_motor.readtext(cropped_img_cv2)
    
    # Metinleri al ve birleştir
    result = ' '.join([text for (_, text, _) in plate])
    
    # Metni veritabanına kaydet
    save_plate(db_name, result)

    return result

# Veritabanına plaka kaydetme
def save_plate(db_name, plate_text):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute("SELECT 1 FROM plakalar WHERE Plate = ?", (plate_text,))
    result = c.fetchone()
    
    if result is None:
        c.execute("INSERT INTO plakalar (Plate) VALUES (?)", (plate_text,))
        conn.commit()
        print(f"'{plate_text}' veritabanına kaydedildi.")
    else:
        print(f"'{plate_text}' zaten veritabanında mevcut, kaydedilmedi.")
    
    conn.close()



# Video karelerini işle
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    # Model ile tespit et
    results = model.predict(source=frame, save=False)

    # Tespit edilen plakaları kırp ve OCR ile işleyip kaydet
    for result in results:
        boxes = result.boxes.xyxy  # Detected bounding boxes
        for box in boxes:
            xmin, ymin, xmax, ymax = map(int, box[:4])
            cropped_img = Image.fromarray(frame[ymin:ymax, xmin:xmax])

            # OCR işlemi ve veritabanına kaydetme
            detected_text = perform_ocr_and_save(cropped_img, db_name, ocr_motor)
            print(f"Tespit edilen plaka metni: {detected_text}")

cap.release()
print("Video işleme tamamlandı.")
