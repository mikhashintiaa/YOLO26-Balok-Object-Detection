# YOLO26 Balok Object Detection

Implementasi **Object Detection menggunakan YOLO26n** untuk mendeteksi beberapa jenis balok dan papan balok. Proyek ini mencakup proses persiapan dataset, anotasi format YOLO, konversi YOLO-COCO, pembagian dataset, training model, hyperparameter tuning, evaluasi, serta pengujian model terbaik.

## Identitas

| Informasi | Keterangan |
|---|---|
| Nama | Mikha Shintia Sitorus |
| NIM | 4222401060 |
| Model | YOLO26n |
| Framework | Ultralytics |
| Task | Object Detection |

---

## 1. Dataset

Dataset yang digunakan merupakan dataset objek balok yang telah melalui proses seleksi untuk membuang gambar yang blur, kurang jelas, atau kurang layak digunakan.

Dataset final terdiri dari **200 gambar** dengan distribusi seimbang sebanyak **50 gambar untuk setiap kelas**.

### Kelas Objek

| Class ID | Nama Kelas | Jumlah Data |
|---:|---|---:|
| 0 | `balok_hijautua` | 50 |
| 1 | `balok_hitam` | 50 |
| 2 | `balok_merahmuda` | 50 |
| 3 | `papan_balok` | 50 |
|  | **Total** | **200** |

Setiap gambar memiliki satu anotasi bounding box dalam format YOLO:

```text
class_id x_center y_center width height
```

Seluruh koordinat bounding box dinormalisasi pada rentang 0 sampai 1.

### Contoh Anotasi Dataset

![Contoh anotasi dataset](README_ASSETS/01_contoh_anotasi_4kelas.jpg)

---

## 2. Pemeriksaan Anotasi

Pemeriksaan anotasi dilakukan menggunakan:

```bash
python3 01_cek_anotasi.py dataset_yolo
```

Hasil pemeriksaan:

```text
Gambar          : 200
Tanpa file label: 0
Label kosong    : 0

Jumlah kotak per kelas:
balok_hijautua  : 50
balok_hitam     : 50
balok_merahmuda : 50
papan_balok     : 50

0 masalah ditemukan.
```

Hasil tersebut menunjukkan bahwa seluruh gambar memiliki file anotasi dan tidak ditemukan kesalahan format label.

---

## 3. Konversi Format YOLO ke COCO

Dataset YOLO kemudian dikonversi menjadi format COCO menggunakan:

```bash
python3 02_yolo_ke_coco.py dataset_yolo
```

Hasil:

```text
200 gambar, 200 kotak, 4 kategori
```

File COCO disimpan sebagai:

```text
dataset_yolo/annotations_coco.json
```

Tahap ini digunakan untuk mempelajari pengelolaan dataset dan perbedaan struktur anotasi antara YOLO dan COCO.

---

## 4. Konversi COCO Kembali ke YOLO

Dataset COCO kemudian dikonversi kembali ke format YOLO menggunakan:

```bash
python3 03_coco_ke_yolo.py \
dataset_yolo/annotations_coco.json \
hasil_yolo
```

Hasil:

```text
200 file label dibuat di hasil_yolo/labels
```

Jumlah file diperiksa menggunakan:

```bash
find hasil_yolo/labels -type f -name "*.txt" | wc -l
```

Hasil:

```text
200
```

Kelas yang dihasilkan tetap:

```text
balok_hijautua
balok_hitam
balok_merahmuda
papan_balok
```

---

## 5. Pembagian Dataset

Dataset kemudian dibagi menjadi data **training, validation, dan testing**.

Pembagian yang digunakan:

| Dataset | Persentase | Jumlah |
|---|---:|---:|
| Train | 70% | 140 |
| Validation | 20% | 40 |
| Test | 10% | 20 |
| **Total** | **100%** | **200** |

Struktur dataset hasil pembagian:

```text
dataset_v1/
├── data.yaml
├── images/
│   ├── train/
│   ├── val/
│   └── test/
└── labels/
    ├── train/
    ├── val/
    └── test/
```

Isi `data.yaml`:

```yaml
path: dataset_v1
train: images/train
val: images/val
test: images/test

names:
  0: balok_hijautua
  1: balok_hitam
  2: balok_merahmuda
  3: papan_balok
```

---

## 6. Konfigurasi Training

Training dilakukan menggunakan **YOLO26n** dengan Ultralytics.

Konfigurasi dasar:

| Parameter | Nilai |
|---|---|
| Model | YOLO26n |
| Epoch | 30 |
| Batch Size | 16 |
| Image Size | 416 |
| Task | Detection |
| Train Data | 140 gambar |
| Validation Data | 40 gambar |
| Test Data | 20 gambar |

Training dilakukan pada:

```text
CPU: AMD Ryzen 5 7520U with Radeon Graphics
```

Eksperimen dijalankan menggunakan:

```bash
python 06_latih_bandingkan.py \
--nim 4222401060 \
--nama "Mikha Shintia Sitorus" \
--data dataset_v1/data.yaml \
--model yolo26n \
--epochs 30 \
--imgsz 416 \
--batch 16 \
--device cpu
```

---

# 7. Eksperimen

Tiga eksperimen dilakukan untuk membandingkan pengaruh pretrained weight dan perubahan hyperparameter.

## E1 - Pretrained

Eksperimen pertama menggunakan model:

```text
yolo26n.pt
```

dengan pretrained weight.

Konfigurasi:

```text
Pretrained : True
Epoch      : 30
Image Size : 416
Batch Size : 16
```

### Hasil Training E1

![Hasil E1](README_ASSETS/02_E1_results.png)

Hasil validation:

| Metric | Nilai |
|---|---:|
| Precision | 0.992 |
| Recall | 1.000 |
| mAP50 | 0.995 |
| mAP50-95 | **0.976** |
| Inference Time | 20.9 ms |
| Training Time | 10.8 menit |

---

## E2 - Scratch

Eksperimen kedua menggunakan arsitektur YOLO26n tanpa pretrained weight.

Model dibuat menggunakan:

```text
yolo26n.yaml
```

Konfigurasi:

```text
Pretrained : False
Epoch      : 30
Image Size : 416
Batch Size : 16
```

Model pada eksperimen ini harus mempelajari feature extraction dan object detection dari awal hanya menggunakan dataset yang tersedia.

### Hasil Training E2

![Hasil E2](README_ASSETS/03_E2_results.png)

Hasil validation:

| Metric | Nilai |
|---|---:|
| Precision | 0.839 |
| Recall | 0.898 |
| mAP50 | 0.952 |
| mAP50-95 | 0.634 |
| Inference Time | 21.9 ms |
| Training Time | 10.7 menit |

---

## E3 - Hyperparameter Tuning

Eksperimen ketiga menggunakan pretrained weight yang sama seperti E1, tetapi dilakukan perubahan pada satu hyperparameter.

Hyperparameter yang diubah adalah:

```text
Image Size
416 → 640
```

Konfigurasi:

```text
Pretrained : True
Epoch      : 30
Image Size : 640
Batch Size : 16
```

Parameter lain dipertahankan agar perubahan performa dapat dibandingkan secara adil terhadap eksperimen E1.

### Hasil Training E3

![Hasil E3](README_ASSETS/04_E3_results.png)

Hasil validation:

| Metric | Nilai |
|---|---:|
| Precision | 0.989 |
| Recall | 1.000 |
| mAP50 | 0.995 |
| mAP50-95 | 0.969 |
| Inference Time | 60.8 ms |
| Training Time | 26.1 menit |

---

# 8. Perbandingan Eksperimen

Hasil dari ketiga eksperimen adalah sebagai berikut:

| Eksperimen | Pretrained | Image Size | mAP50 | mAP50-95 | Precision | Recall | Inference |
|---|---|---:|---:|---:|---:|---:|---:|
| **E1 Pretrained** | Ya | 416 | **0.995** | **0.976** | **0.992** | **1.000** | **20.9 ms** |
| E2 Scratch | Tidak | 416 | 0.952 | 0.634 | 0.839 | 0.898 | 21.9 ms |
| E3 Tuning | Ya | 640 | **0.995** | 0.969 | 0.989 | **1.000** | 60.8 ms |

### Grafik Perbandingan Akurasi

![Perbandingan akurasi](README_ASSETS/05_perbandingan_akurasi_E1_E2_E3.png)

### Grafik Perbandingan Waktu Inferensi

![Perbandingan inference](README_ASSETS/06_perbandingan_inference_time.png)

---

# 9. Analisis Eksperimen

## Perbandingan E1 dan E2

Eksperimen E1 memperoleh nilai `mAP50-95 = 0.976`, sedangkan E2 memperoleh `mAP50-95 = 0.634`.

Perbedaan utama antara kedua eksperimen adalah penggunaan pretrained weight.

Pada E1, YOLO26n telah memiliki weight hasil pembelajaran sebelumnya sehingga model sudah memiliki kemampuan awal dalam mengenali berbagai feature visual seperti bentuk, edge, tekstur, dan pola objek.

Sebaliknya, E2 menggunakan model scratch sehingga seluruh parameter model harus dipelajari dari awal.

Karena dataset pada proyek ini hanya terdiri dari 200 gambar, proses training dari awal memiliki informasi yang lebih terbatas. Hal ini menyebabkan performa E2 lebih rendah dibandingkan E1.

Dengan demikian, penggunaan **transfer learning menggunakan pretrained model memberikan peningkatan performa yang signifikan** pada dataset yang relatif kecil.

---

## Perbandingan E1 dan E3

E3 menggunakan pretrained model yang sama seperti E1, tetapi ukuran gambar dinaikkan dari:

```text
416 × 416
```

menjadi:

```text
640 × 640
```

Secara teori, resolusi gambar yang lebih tinggi dapat memberikan informasi visual yang lebih detail.

Namun hasil eksperimen menunjukkan:

```text
E1 mAP50-95 = 0.976
E3 mAP50-95 = 0.969
```

Artinya peningkatan resolusi tidak memberikan peningkatan akurasi pada dataset ini.

Selain itu, waktu inference meningkat dari:

```text
20.9 ms → 60.8 ms
```

Sedangkan waktu training meningkat dari:

```text
10.8 menit → 26.1 menit
```

Dengan demikian, penggunaan `imgsz=640` membutuhkan komputasi yang jauh lebih besar tetapi tidak menghasilkan peningkatan akurasi.

Untuk dataset ini, `imgsz=416` memberikan keseimbangan yang lebih baik antara akurasi dan kecepatan.

---

# 10. Model Terbaik

Pemilihan model dilakukan berdasarkan nilai **mAP50-95 pada validation set**.

Hasil:

```text
E1 Pretrained : 0.976
E2 Scratch    : 0.634
E3 Tuning     : 0.969
```

Model terbaik adalah:

```text
E1_pretrained
```

dengan:

```text
mAP50    = 0.995
mAP50-95 = 0.976
Precision = 0.992
Recall    = 1.000
```

Weight model terbaik tersimpan pada:

```text
hasil_praktik/E1_pretrained/weights/best.pt
```

---

# 11. Precision-Recall Curve

Precision-Recall Curve digunakan untuk melihat hubungan antara nilai precision dan recall dari model pada berbagai confidence threshold.

![PR Curve](README_ASSETS/08_PR_curve_E1.png)

Kurva tersebut menunjukkan performa model E1 dalam mempertahankan precision dan recall pada proses object detection.

---

# 12. F1 Curve

F1 Score merupakan harmonic mean antara precision dan recall.

![F1 Curve](README_ASSETS/09_F1_curve_E1.png)

Kurva F1 membantu melihat confidence threshold yang memberikan keseimbangan terbaik antara precision dan recall.

---

# 13. Pengujian Model Terbaik

Setelah model terbaik ditentukan menggunakan validation set, model kemudian diuji **satu kali pada test set**.

Test set terdiri dari:

```text
20 gambar
```

Hasil evaluasi:

| Metric | Hasil Test |
|---|---:|
| mAP50 | **0.995** |
| mAP50-95 | **0.991** |

Hasil tersebut menunjukkan bahwa model memiliki performa yang sangat baik pada data yang tidak digunakan selama proses training maupun pemilihan model.

---

## Visualisasi Hasil Test

Prediksi pada test set dilakukan dengan:

```bash
yolo detect predict \
model=hasil_praktik/E1_pretrained/weights/best.pt \
source=dataset_v1/images/test \
imgsz=416 \
conf=0.25 \
device=cpu \
save=True
```

Sebanyak **20 gambar test berhasil diproses**.

Contoh hasil deteksi untuk empat kelas:

![Hasil test](README_ASSETS/07_hasil_test_4kelas.jpg)

Pada pengujian visual, model mampu mendeteksi objek dari kelas:

```text
balok_hijautua
balok_hitam
balok_merahmuda
papan_balok
```

---

# 14. Struktur Repository

```text
YOLO26-Balok-Object-Detection/
│
├── 00_ambil_subset_coco.py
├── 01_cek_anotasi.py
├── 02_yolo_ke_coco.py
├── 03_coco_ke_yolo.py
├── 05_split_dataset_yolo.py
├── 06_latih_bandingkan.py
├── 07_siapkan_gambar_readme.py
│
├── dataset_yolo/
│   ├── images/
│   ├── labels/
│   ├── classes.txt
│   ├── annotations_coco.json
│   └── cek_visual/
│
├── hasil_yolo/
│   ├── labels/
│   └── classes.txt
│
├── dataset_v1/
│   ├── data.yaml
│   ├── images/
│   │   ├── train/
│   │   ├── val/
│   │   └── test/
│   └── labels/
│       ├── train/
│       ├── val/
│       └── test/
│
├── hasil_praktik/
│   ├── E1_pretrained/
│   │   ├── results.png
│   │   └── weights/
│   │       └── best.pt
│   │
│   ├── E2_scratch/
│   │   ├── results.png
│   │   └── weights/
│   │
│   ├── E3_tuning/
│   │   ├── results.png
│   │   └── weights/
│   │
│   └── TEST_E1/
│
├── README_ASSETS/
│   ├── 01_contoh_anotasi_4kelas.jpg
│   ├── 02_E1_results.png
│   ├── 03_E2_results.png
│   ├── 04_E3_results.png
│   ├── 05_perbandingan_akurasi_E1_E2_E3.png
│   ├── 06_perbandingan_inference_time.png
│   ├── 07_hasil_test_4kelas.jpg
│   ├── 08_PR_curve_E1.png
│   └── 09_F1_curve_E1.png
│
├── hasil_praktik_4222401060.txt
├── hasil_praktik_4222401060.csv
└── README.md
```

---

# 15. Program

### Pemeriksaan Anotasi

```bash
python3 01_cek_anotasi.py dataset_yolo
```

### YOLO ke COCO

```bash
python3 02_yolo_ke_coco.py dataset_yolo
```

### COCO ke YOLO

```bash
python3 03_coco_ke_yolo.py \
dataset_yolo/annotations_coco.json \
hasil_yolo
```

### Split Dataset

```bash
python3 05_split_dataset_yolo.py dataset_yolo dataset_v1
```

### Training dan Perbandingan

```bash
python 06_latih_bandingkan.py \
--nim 4222401060 \
--nama "Mikha Shintia Sitorus" \
--data dataset_v1/data.yaml \
--model yolo26n \
--epochs 30 \
--imgsz 416 \
--batch 16 \
--device cpu
```

---

# 16. Kesimpulan

Berdasarkan pengujian yang dilakukan, **E1 Pretrained merupakan konfigurasi terbaik** untuk dataset balok pada proyek ini.

Model memperoleh:

```text
Validation
mAP50    : 0.995
mAP50-95 : 0.976
Precision: 0.992
Recall   : 1.000
```

dan pada test set memperoleh:

```text
mAP50    : 0.995
mAP50-95 : 0.991
```

Eksperimen juga menunjukkan bahwa pretrained weight sangat membantu pada dataset berukuran relatif kecil. Model yang dilatih dari awal pada E2 menghasilkan performa yang lebih rendah.

Peningkatan ukuran input dari 416 menjadi 640 pada E3 juga tidak meningkatkan akurasi. Sebaliknya, waktu training dan inference menjadi jauh lebih tinggi.

Oleh karena itu, konfigurasi **YOLO26n pretrained dengan `imgsz=416`** dipilih sebagai konfigurasi terbaik karena memberikan kombinasi akurasi tinggi dan kebutuhan komputasi yang lebih rendah.

---

## Author

**Mikha Shintia Sitorus**  
NIM **4222401060**
