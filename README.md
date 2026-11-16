# Bias Kebocoran Data akibat SMOTE pada Prediksi Stroke

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23887242.svg)](https://doi.org/10.5281/zenodo.23887242)

Kode dan hasil eksperimen untuk artikel:

> Ade Rumintarsih. *Bias Kebocoran Data akibat SMOTE pada Prediksi Stroke: Re-evaluasi dengan Nested Cross-Validation dan Kalibrasi.* Naskah revisi untuk *Journal of Informatics and Electronics Engineering* (JIEE), 2026.

Banyak studi pada *Stroke Prediction Dataset* Kaggle (5.110 data, prevalensi stroke 4,9%) melaporkan akurasi di atas 95%. Repositori ini mengukur bias yang muncul bila *oversampling* diterapkan **sebelum** data dibagi menjadi data latih dan data uji, lalu mengevaluasi ulang model dengan prosedur yang bebas kebocoran.

## Temuan utama

| Skenario (Random Forest, data uji 20% yang sama) | Akurasi | ROC-AUC | PR-AUC | Recall |
|---|---|---|---|---|
| Bocor: SMOTE sebelum split (data uji campuran) | 0,967 | 0,996 | 0,996 | 0,977 |
| Bocor: SMOTE sebelum split (hanya pasien asli) | 0,944 | 0,955 | 0,483 | 0,634 |
| Bocor: random oversampling sebelum split | 0,992 | 1,000 | 1,000 | 1,000 |
| Benar: SMOTE hanya pada data latih | 0,940 | 0,769 | 0,135 | 0,180 |

- 931 dari 972 kasus positif (95,8%) pada data uji skenario bocor adalah sampel sintetis. Pasien stroke asli di data uji pun memiliki tetangga sintetis di data latih, sehingga kebocoran tetap terlihat setelah efek prevalensi dipisahkan.
- Dengan *nested cross-validation*, kinerja realistis berada pada ROC-AUC 0,80–0,84 dan PR-AUC 0,14–0,19, hampir setara dengan regresi logistik yang hanya memakai usia (ROC-AUC 0,833).
- Pada uji primer Nadeau–Bengio dengan koreksi Holm, tidak ada efek optimasi *hyperparameter* yang signifikan; Random Forest terbaik tidak lebih baik daripada regresi logistik (p = 0,765).
- Koreksi ketidakseimbangan kelas tidak menaikkan *recall* pada ambang Youden yang dipilih dari data latih, tetapi merusak kalibrasi (Brier score 0,042 → 0,146–0,181; *intercept* kalibrasi sekitar −2,6 sampai −3,0).
- Model yang dipilih hanya dari data latih (HGB tanpa penanganan) mencapai ROC-AUC 0,826, *recall* 0,800, dan spesifisitas 0,788 pada data uji, dengan *net benefit* pada ambang 2–16%.

## Struktur

```
notebooks/
  01_eksperimen_utama.ipynb              eksperimen 1–3, gambar
  02_revisi_M1_M3.ipynb                  seleksi model hanya dari data latih, SMOTE-NC, statistik
  03_kalibrasi_DCA_uji_terkoreksi.ipynb  Brier skill score, slope kalibrasi, decision curve, Nadeau–Bengio
  04_revisi_reviewer.ipynb               analisis tambahan untuk tanggapan reviewer (lihat tabel di bawah)
  05_verifikasi_imblearn.ipynb           perbandingan SMOTE/SMOTE-NC buatan sendiri dengan imbalanced-learn
literature/
  skrining_literatur.py                  skrining Scopus yang dapat dijalankan ulang
  eid_6843_dokumen_unik.csv              daftar EID korpus skrining (untuk membangun ulang korpus)
  kandidat_95.csv                        95 artikel kandidat hasil penyaringan otomatis
  verifikasi_kandidat_artikel.csv        hasil verifikasi manual setiap kandidat (tanpa abstrak)
results/                                 hasil notebook 01–03
results/revisi1/                         hasil notebook 04 dan 05
figures/                                 gambar naskah
data/                                    letakkan dataset di sini (tidak disertakan)
```

## Revisi 1 (tanggapan reviewer JIEE)

| Analisis tambahan | File hasil di `results/revisi1/` |
|---|---|
| BMI kosong dan indikator *missing*, recall/MCC pada ambang Youden, *intercept*/*slope* kalibrasi, IK per pengulangan | `r04_nested_ringkasan_youden_kalibrasi.csv`, `r04_ringkasan.json` |
| Selisih PR-AUC per fold, uji primer Nadeau–Bengio + Holm | `r04_selisih_per_fold_tuning.csv` |
| Stabilitas peringkat (bootstrap fold) | `r04_stabilitas_peringkat.csv` |
| Skenario bocor diuji hanya pada pasien asli, *lift* PR-AUC, *random oversampling* sebelum split | `r04_skenario_prevalensi_ros.csv` |
| Variasi 20 seed skenario benar | `r04_variasi_seed_skenarioB.csv` |
| Baseline regresi logistik usia saja | `r04_usia_saja_per_fold.csv`, `r04_ringkasan.json` |
| *Permutation importance* pada OOF data latih dan data uji | `r04_permutation_importance_oof_vs_uji.csv` |
| Verifikasi terhadap imbalanced-learn | `verifikasi_imblearn/` |

## Cara menjalankan

1. Pasang paket: `pip install -r requirements.txt` (notebook 05 juga memerlukan `pip install imbalanced-learn`).
2. Unduh dataset dari Kaggle (lihat `data/README.md`) dan simpan sebagai `data/healthcare-dataset-stroke-data.csv`.
3. Jalankan notebook 01, 02, 03, 04, lalu 05 dari folder `notebooks/` (*Run All*). Bagian nested CV pada notebook 04 memerlukan beberapa jam.

`SEED = 42` mereproduksi angka di naskah. Skrining literatur memerlukan file ekspor Scopus (`export_*.csv`) di `data/`; file tersebut tidak dibagikan karena berlisensi Elsevier, tetapi korpusnya dapat dibangun ulang dari `literature/eid_6843_dokumen_unik.csv`. Kolom abstrak tidak disertakan karena alasan hak cipta.

## Catatan

- SMOTE dan SMOTE-NC diimplementasikan langsung mengikuti Chawla dkk. (2002) agar dapat ditempatkan di dalam *pipeline* bersarang; kesetaraannya dengan imbalanced-learn diperiksa di notebook 05 (selisih rata-rata ROC-AUC ≤ 0,005 dan PR-AUC ≤ 0,004 pada 5-fold CV × 5 seed, lebih kecil daripada variasi antar-seed).
- Verifikasi artikel pada `literature/` dilakukan oleh satu penilai pada abstrak dan bersifat indikatif.

## Sitasi

Arsip kode: Ade Rumintarsih (2026). *KEBOCORAN-DATA-STROKE* [Kode dan data hasil]. Zenodo. https://doi.org/10.5281/zenodo.23887242

## Lisensi

Kode dirilis dengan lisensi MIT (lihat `LICENSE`). Dataset mengikuti lisensi sumber aslinya di Kaggle.
