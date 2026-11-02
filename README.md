# Bias Kebocoran Data akibat SMOTE pada Prediksi Stroke

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23887243.svg)](https://doi.org/10.5281/zenodo.23887243)

Kode dan hasil eksperimen untuk artikel:

> Ade Rumintarsih. *Bias Kebocoran Data akibat SMOTE pada Prediksi Stroke: Re-evaluasi dengan Nested Cross-Validation dan Kalibrasi.* Naskah dikirim ke *Journal of Informatics and Electronics Engineering* (JIEE), 2026.

Banyak studi pada *Stroke Prediction Dataset* Kaggle (5.110 data, prevalensi stroke 4,9%) melaporkan akurasi di atas 95%. Repositori ini menguji dugaan bahwa angka tersebut berasal dari SMOTE yang diterapkan **sebelum** data dibagi menjadi data latih dan data uji, lalu mengevaluasi ulang model dengan prosedur yang bebas kebocoran.

## Temuan utama

| Skenario (Random Forest, data uji 20%) | Akurasi | ROC-AUC | PR-AUC | Recall |
|---|---|---|---|---|
| Bocor: SMOTE sebelum split | 0,967 | 0,996 | 0,996 | 0,977 |
| Benar: SMOTE hanya pada data latih | 0,940 | 0,769 | 0,135 | 0,180 |

- 931 dari 972 kasus positif (95,8%) pada data uji skenario bocor adalah sampel sintetis.
- Dengan *nested cross-validation*, kinerja realistis berada pada ROC-AUC 0,80–0,84 dan PR-AUC 0,14–0,19.
- Random Forest terbaik tidak lebih baik daripada regresi logistik (uji Wilcoxon berpasangan, p = 0,375).
- Koreksi ketidakseimbangan kelas merusak kalibrasi; kalibrasi isotonik menurunkan Brier score dari 0,164 menjadi 0,042.

## Struktur

```
notebooks/
  01_eksperimen_utama.ipynb   skrining literatur, eksperimen 1–3, gambar
  02_revisi_M1_M3.ipynb       seleksi model hanya dari data latih (M1), SMOTE-NC (M3), statistik lengkap
results/                      CSV/JSON hasil eksperimen (dipakai di naskah)
figures/                      gambar naskah
literature/                   metadata skrining 81 artikel Scopus (tanpa abstrak)
data/                         letakkan dataset di sini (tidak disertakan)
```

## Cara menjalankan

1. Pasang paket: `pip install -r requirements.txt`
2. Unduh dataset dari Kaggle (lihat `data/README.md`) dan simpan sebagai `data/healthcare-dataset-stroke-data.csv`.
3. Jalankan `notebooks/01_eksperimen_utama.ipynb`, lalu `notebooks/02_revisi_M1_M3.ipynb` (*Run All*). Hasil tersimpan di `results/`.

Pengaturan bawaan (`USE_OPTUNA = False`, `USE_EXTRA_MODELS = False`, `SEED = 42`) mereproduksi angka di naskah. Bagian skrining literatur hanya berjalan bila file ekspor Scopus (`export_*.csv`) diletakkan di `data/`; file tersebut tidak dibagikan karena berlisensi Elsevier.

## Catatan

- Label risiko kebocoran pada `literature/` berasal dari aturan kata kunci pada abstrak dan perlu diverifikasi dengan teks lengkap.
- SMOTE diimplementasikan langsung mengikuti Chawla dkk. (2002) agar tidak bergantung pada `imbalanced-learn`.

## Sitasi

Arsip kode: Ade Rumintarsih (2026). *KEBOCORAN-DATA-STROKE* [Kode dan data hasil]. Zenodo. https://doi.org/10.5281/zenodo.23887243

## Lisensi

Kode dirilis dengan lisensi MIT (lihat `LICENSE`). Dataset mengikuti lisensi sumber aslinya di Kaggle.
