
# License Plate Recognition Project / Plaka Tanıma Projesi

## 📌 Languages / Diller
- [English](#english)
- [Türkçe](#türkçe)

---

## English

This project performs license plate detection from images or videos using the YOLOv8 model. Detected plates are converted into digital text using OCR (Optical Character Recognition) and then stored in an SQLite database.

### Table of Contents

- [Requirements](#requirements)
- [Project Workflow](#project-workflow)
- [Training File (train_yolov8.ipynb)](#training-file-train_yolov8ipynb)
- [Dataset](#dataset)
- [OCR (Optical Character Recognition)](#ocr-optical-character-recognition)
- [Database - SQLite](#database---sqlite)

### Requirements

- Python 3.7+
- YOLOv8
- OpenCV
- Roboflow (for dataset)
- SQLite
- Tesseract OCR (for OCR operations)

Install dependencies:
```bash
pip install ultralytics opencv-python-headless sqlite3 pytesseract
```

### Project Workflow

1. License plates are detected using the YOLOv8 model.
2. Detected plates are converted to digital text via OCR.
3. The extracted text is stored in an SQLite database.

### Training File (train_yolov8.ipynb)

The **train_yolov8.ipynb** file contains the training process of the YOLOv8 model for license plate recognition. After training, the model is used for detection.

The **data.yaml** file defines the path to the dataset used during training.

### Dataset

The project uses a dataset from **Roboflow**. You can download it from [Roboflow License Plate Dataset](https://universe.roboflow.com/mochoye/license-plate-detector-ogxxg) and use it for model training.

### OCR (Optical Character Recognition)

OCR converts text from images into digital format. Detected license plates are processed using **Tesseract OCR** to extract textual information.

### Database - SQLite

SQLite is a lightweight, serverless database system. The license plate texts extracted by OCR are saved into SQLite for easy access and management.

---

## Türkçe

Bu projede, YOLOv8 modeli kullanılarak resim veya video üzerinden plaka tespiti yapılır. Tespit edilen plakalar, OCR (Optik Karakter Tanıma) ile dijital metin haline getirilir ve son olarak SQLite veritabanına kaydedilir.

### İçindekiler

- [Gereksinimler](#gereksinimler)
- [Proje Akışı](#proje-akışı)
- [Eğitim Dosyası (train_yolov8.ipynb)](#eğitim-dosyası-train_yolov8ipynb)
- [Veri Seti](#veri-seti)
- [OCR (Optical Character Recognition)](#ocr-optical-character-recognition)
- [Veritabanı - SQLite](#veritabanı---sqlite)

### Gereksinimler

- Python 3.7+
- YOLOv8
- OpenCV
- Roboflow (veri seti için)
- SQLite
- Tesseract OCR (OCR işlemleri için)

Gereksinimlerinizi yüklemek için:
```bash
pip install ultralytics opencv-python-headless sqlite3 pytesseract
```

### Proje Akışı

1. YOLOv8 modeli kullanılarak görsellerdeki plakalar tespit edilir.
2. Tespit edilen plakalar OCR işlemi ile dijital metin haline dönüştürülür.
3. OCR ile elde edilen plaka bilgileri, SQLite veritabanında saklanır.

### Eğitim Dosyası (train_yolov8.ipynb)

**train_yolov8.ipynb** dosyasında, YOLOv8 modeli ile plaka tanıma işlemi için eğitim yapılır. Model, eğitim tamamlandıktan sonra plaka tespitinde kullanılır. 

**data.yaml** dosyasında veri setinin yolu belirtilir. Bu dosya, modelin eğitim için hangi veri setini kullanacağını tanımlar.

### Veri Seti

Projede, **Roboflow** platformundan alınan bir veri seti kullanılmıştır. [Roboflow Plaka Tanıma Veri Seti](https://universe.roboflow.com/mochoye/license-plate-detector-ogxxg) üzerinden verileri indirerek modeli eğitebilirsiniz.

### OCR (Optical Character Recognition)

Optik Karakter Tanıma (OCR), görsellerdeki metinleri tanıyıp dijital yazıya çevirir. YOLOv8 modeli ile tespit edilen plakalar, OCR işlemi uygulanarak metin haline getirilir. Bu işlem için **Tesseract OCR** kütüphanesi kullanılmıştır.

### Veritabanı - SQLite

SQLite, sunucusuz çalışan hafif bir veritabanı yönetim sistemidir. OCR ile yazıya dökülen plakalar SQLite veritabanında saklanır. Bu sayede plaka bilgilerine erişim ve yönetim kolaylaştırılır.

Veritabanı işlemleri, tespit edilen plakaların kaydedilmesi, güncellenmesi ve gerektiğinde sorgulanmasını sağlar.
