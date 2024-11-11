import ultralytics
from ultralytics import YOLO
import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import torch
import os
import easyocr
import sqlite3

# Sistem uyumluluk kontrolü
ultralytics.checks()

# Veritabanı ve tabloyu oluşturma
def create_table_if_not_exists(db_name):
    """
    Eğer plakalar tablosu yoksa, yeni bir tablo oluşturur.
    """
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    
    # Tabloyu oluştur
    c.execute('''CREATE TABLE IF NOT EXISTS plakalar (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    Plate TEXT UNIQUE
                )''')
    
    conn.commit()
    conn.close()

# Tabloyu oluştur
db_name = 'database/plate_database1.db'
create_table_if_not_exists(db_name)

# YOLO Modelini yükle
model = YOLO('runs/detect/train6/weights/best.pt')

# Görüntüyü yükle
img = Image.open('test_data/plates1.PNG')

# Model ile tahmin yap
test_result = model.predict(img)


# Kırpma ve görüntü gösterme işlemleri için fonksiyon
def crop_save_and_display_objects(img, test_result, save_dir='cropped_objects'):
    """
    Tespit edilen bounding box'lara göre kırpma işlemi yapar, 
    her bir kırpılmış nesneyi kaydeder ve görüntüleri gösterir.
    """
    os.makedirs(save_dir, exist_ok=True)
    cropped_images = []

    for idx, result in enumerate(test_result):
        for box_idx, box in enumerate(result.boxes.xyxy):
            xmin, ymin, xmax, ymax = map(int, box[:4])
            cropped_img = img.crop((xmin, ymin, xmax, ymax))
            cropped_images.append(cropped_img)
            # Kırpılmış görüntüyü RGB'ye dönüştür ve kaydet
            cropped_img = cropped_img.convert("RGB")
            cropped_img.save(f'{save_dir}/cropped_object_{idx}_{box_idx}.jpg')

            fig, axes = plt.subplots(1, 2, figsize=(10, 5))
            axes[0].imshow(img)
            axes[0].set_title("Original Image")
            axes[0].axis('off')

            axes[1].imshow(cropped_img)
            axes[1].set_title(f"Cropped Object {idx}_{box_idx}")
            axes[1].axis('off')
            plt.show()

    return cropped_images


# OCR işlemi için EasyOCR motorunu başlat
ocr_motor = easyocr.Reader(['en', 'tr'])

def perform_ocr_on_image(cropped_img, ocr_motor):
    """
    Kırpılmış bir görüntüde OCR işlemi yapar, tespit edilen metinleri
    kutulara çizer ve tüm metinleri birleştirerek döndürür.
    """
    cropped_img_np = np.array(cropped_img)
    cropped_img_cv2 = cv2.cvtColor(cropped_img_np, cv2.COLOR_RGB2BGR)
    detected_texts = ocr_motor.readtext(cropped_img_cv2)

    # Her bir metni ekrana yazdır ve resme kutu çiz
    for (bbox, text, prob) in detected_texts:
        print(f'Detected Text: {text}, Confidence: {prob:.2f}')

    for (bbox, text, _) in detected_texts:
        top_left, top_right, bottom_right, bottom_left = [tuple(map(int, pt)) for pt in bbox]
        cv2.rectangle(cropped_img_cv2, top_left, bottom_right, (0, 255, 0), 2)
        cv2.putText(cropped_img_cv2, text, (top_left[0], top_left[1] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    img_rgb = cv2.cvtColor(cropped_img_cv2, cv2.COLOR_BGR2RGB)
    plt.imshow(img_rgb)
    plt.axis('off')
    plt.show()

    # Resimdeki yazıları yan yana yazdır
    result_text = ' '.join([text for (_, text, _) in detected_texts])
    print(f'Tespit Edilen Metin: {result_text}')

    # Tüm tespit edilen metinleri birleştir
    return result_text  # OCR sonuçları

# Veritabanına tüm plakaları kaydetmek için fonksiyon
def save_all_plates_to_database(db_name, result_text):
    """
    Bir tespit edilen plaka değerini veritabanına kaydeder.
    """
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    # Aynı plaka varsa kaydetme
    c.execute("SELECT 1 FROM plakalar WHERE Plate = ?", (result_text,))
    if c.fetchone() is None:
        c.execute("INSERT INTO plakalar (Plate) VALUES (?)", (result_text,))
        print(f"'{result_text}' saved to the database.")
    else:
        print(f"'{result_text}' is already in the database.")
    
    conn.commit()
    conn.close()



# Resimdeki tüm plakaları işleme
plate_images = crop_save_and_display_objects(img, test_result)

# Plate images içerisinde her bir resmi OCR ile işleyip veritabanına kaydetme
for plate_img in plate_images:
    if plate_img:
        # OCR ile metin tespiti yap
        detected_texts = perform_ocr_on_image(plate_img, ocr_motor)
        
        # Veritabanına kaydetme
        save_all_plates_to_database(db_name, detected_texts)
