# Plaka Tanıma Projesi

Bu projede, YOLOv8 modeli kullanılarak resim veya video üzerinden plaka tespiti yapılır. Tespit edilen plakalar, OCR (Optik Karakter Tanıma) ile dijital metin haline getirilir ve son olarak SQLite veritabanına kaydedilir.

## İçindekiler

- [Gereksinimler](#gereksinimler)
- [Proje Akışı](#proje-akışı)
- [Eğitim Dosyası (train_yolov8.ipynb)](#eğitim-dosyası-train_yolov8ipynb)
- [Veri Seti](#veri-seti)
- [OCR (Optical Character Recognition)](#ocr-optical-character-recognition)
- [Veritabanı - SQLite](#veritabanı---sqlite)

## Gereksinimler

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

## Proje Akışı

1. YOLOv8 modeli kullanılarak görsellerdeki plakalar tespit edilir.
2. Tespit edilen plakalar OCR işlemi ile dijital metin haline dönüştürülür.
3. OCR ile elde edilen plaka bilgileri, SQLite veritabanında saklanır.

## Eğitim Dosyası (train_yolov8.ipynb)

**train_yolov8.ipynb** dosyasında, YOLOv8 modeli ile plaka tanıma işlemi için eğitim yapılır. Model, eğitim tamamlandıktan sonra plaka tespitinde kullanılır. 

**data.yaml** dosyasında veri setinin yolu belirtilir. Bu dosya, modelin eğitim için hangi veri setini kullanacağını tanımlar.

## Veri Seti

Projede, **Roboflow** platformundan alınan bir veri seti kullanılmıştır. [Roboflow Plaka Tanıma Veri Seti](https://universe.roboflow.com/mochoye/license-plate-detector-ogxxg) üzerinden verileri indirerek modeli eğitebilirsiniz.

## OCR (Optical Character Recognition)

Optik Karakter Tanıma (OCR), görsellerdeki metinleri tanıyıp dijital yazıya çevirir. YOLOv8 modeli ile tespit edilen plakalar, OCR işlemi uygulanarak metin haline getirilir. Bu işlem için **Tesseract OCR** kütüphanesi kullanılmıştır.

## Veritabanı - SQLite

SQLite, sunucusuz çalışan hafif bir veritabanı yönetim sistemidir. OCR ile yazıya dökülen plakalar SQLite veritabanında saklanır. Bu sayede plaka bilgilerine erişim ve yönetim kolaylaştırılır. 

Veritabanı işlemleri, tespit edilen plakaların kaydedilmesi, güncellenmesi ve gerektiğinde sorgulanmasını sağlar.


