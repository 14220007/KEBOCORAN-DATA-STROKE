"""Skrining literatur Scopus (reproduksi alur Gbr. skrining).
Masukan : folder berisi tiga file ekspor Scopus (export_*.csv, diunduh 8 Oktober 2026), contoh: python skrining_literatur.py ../data
Keluaran: kandidat_95.csv (artikel kandidat) dan ringkasan jumlah pada tiap tahap.
Verifikasi manual tiap kandidat tersimpan di verifikasi_kandidat_artikel.csv."""
import pandas as pd, glob, re, sys, os
D = sys.argv[1] if len(sys.argv) > 1 else "."
fs = sorted(glob.glob(os.path.join(D, "export_*.csv")))
d = pd.concat([pd.read_csv(f, low_memory=False) for f in fs]); print("Rekaman ekspor:", len(d))
d["key"] = d.EID.fillna(d.Title.str.lower()); u = d.drop_duplicates("key").copy()
print("Dokumen unik (deduplikasi EID):", len(u), "| duplikat:", len(d) - len(u))
u["txt"] = (u.Title.fillna("") + " " + u.Abstract.fillna("") + " " + u["Author Keywords"].fillna("")).str.lower()
ATURAN = {
 "dataset_kaggle": r"kaggle|healthcare-dataset|5110|5,110|stroke prediction dataset|fedesoriano",
 "judul_stroke": r"stroke",
 "judul_citra": r"\bct\b|mri|imaging|computed tomography|image|pet\b",
 # indikator pelaporan pada abstrak (untuk karakterisasi, diverifikasi manual)
 "oversampling": r"smote|oversampl|adasyn|imbalanc",
 "tuning": r"hyperparamet|grid search|random search|bayesian optim|optuna|tuning",
 "kebocoran": r"leakage|leak",
 "kalibrasi": r"calibrat",
 "pr_auc": r"pr-auc|auprc|precision-recall curve|average precision",
 "mcc": r"matthews|\bmcc\b",
}
AKURASI = r"accuracy[^.;]{0,60}?(\d{2,3}(?:\.\d+)?)\s*%|(\d{2,3}(?:\.\d+)?)\s*%[^.;]{0,30}?accuracy"
s1 = u[u.txt.str.contains(ATURAN["dataset_kaggle"])]; print("Menyebut dataset:", len(s1))
s2 = s1[s1.Title.str.lower().str.contains(ATURAN["judul_stroke"])]; print("Judul memuat stroke:", len(s2))
s3 = s2[~s2.Title.str.lower().str.contains(ATURAN["judul_citra"])]; print("Judul bukan citra (kandidat):", len(s3))
for k in list(ATURAN)[3:]: s3[k] = s3.txt.str.contains(ATURAN[k])
def akurasi(t):
    v = [float(a or b) for a, b in re.findall(AKURASI, t)]; v = [x for x in v if 50 <= x <= 100]
    return max(v) if v else None
s3["akurasi_otomatis"] = s3.txt.map(akurasi)
s3[["EID", "Year", "Title", "Source title", "DOI", "akurasi_otomatis"] + list(ATURAN)[3:]].to_csv("kandidat_95.csv", index=False)
print("Distribusi tahun dokumen unik:", u.Year.value_counts().sort_index().to_dict())
# Tahap verifikasi manual (hasil pembacaan abstrak satu per satu)
vf = os.path.join(os.path.dirname(os.path.abspath(__file__)), "verifikasi_kandidat_artikel.csv")
if os.path.exists(vf):
    v = pd.read_csv(vf); inc = v[v.Masuk_analisis == "Ya"]; acc = inc.Akurasi_verifikasi.dropna()
    print("Dikeluarkan saat verifikasi:", (v.Masuk_analisis == "Tidak").sum(), v[v.Masuk_analisis == "Tidak"].Kategori.value_counts().to_dict())
    print("Dianalisis:", len(inc), inc.Kategori.value_counts().to_dict())
    print(f"Abstrak dengan akurasi: {len(acc)}; >=95%: {(acc>=95).sum()} ({(acc>=95).mean():.0%}); >=99%: {(acc>=99).sum()}; median {acc.median():.1f}%")
