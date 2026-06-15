# =========================================================
# Pembasmi Spam Judol - Training Model Klasifikasi
# =========================================================

import re
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix

# =========================================================
# 2. LOAD DATASET
# =========================================================
df = pd.read_csv("ML/dataset.csv")

print("Jumlah data:", len(df))
print(df["label"].value_counts())
print(df.head())

# =========================================================
# 3. PREPROCESSING TEKS
# =========================================================
# Mapping karakter "leetspeak" / penyamaran umum -> huruf normal
LEET_MAP = {
    "0": "o",
    "1": "i",
    "3": "e",
    "4": "a",
    "5": "s",
    "7": "t",
    "8": "b",
    "9": "g",
    "@": "a",
    "$": "s",
}

def normalize_leet(text):
    def fix_token(token):
        # buang digit di akhir token (angka varian: GACOR77 -> GACOR)
        token = re.sub(r"\d+$", "", token)
        has_letter = any(c.isalpha() for c in token)
        has_digit = any(c.isdigit() for c in token)
        if has_letter and has_digit:
            token = "".join(LEET_MAP.get(ch, ch) for ch in token)
        return token
    return " ".join(fix_token(tok) for tok in text.split())

def clean_text(text):
    text = text.lower()
    text = re.sub(r"http\S+|www\.\S+", " ", text)       # hapus URL
    text = re.sub(r"[^a-z0-9\s]", " ", text)             # hapus simbol/emoji
    text = re.sub(r"\s+", " ", text).strip()             # rapikan spasi
    text = normalize_leet(text)                          # buang angka varian + normalisasi leetspeak sisa
    text = re.sub(r"\b\d+\b", "", text)                  # hapus token angka murni (nominal, dll)
    text = re.sub(r"\s+", " ", text).strip()
    return text

df["clean_text"] = df["text"].apply(clean_text)
print(df[["text", "clean_text"]].head())

# =========================================================
# 4. SPLIT DATA
# =========================================================
X = df["clean_text"]
y = df["label"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# =========================================================
# 5. FEATURE EXTRACTION (TF-IDF)
# =========================================================
vectorizer = TfidfVectorizer(
    ngram_range=(1, 2),   # unigram + bigram
    min_df=1,
    max_features=5000
)

X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# =========================================================
# 6. TRAINING MODEL
# =========================================================
model = LogisticRegression(max_iter=1000, class_weight="balanced")
model.fit(X_train_vec, y_train)

# =========================================================
# 7. EVALUASI
# =========================================================
y_pred = model.predict(X_test_vec)

print("\n=== Classification Report ===")
print(classification_report(y_test, y_pred, target_names=["bukan_judol", "judol"]))

print("\n=== Confusion Matrix ===")
print(confusion_matrix(y_test, y_pred))

# =========================================================
# 8. SIMPAN MODEL & VECTORIZER
# =========================================================
joblib.dump(model, "model_judol.joblib")
joblib.dump(vectorizer, "vectorizer_judol.joblib")

print("\nModel dan vectorizer berhasil disimpan!")

# =========================================================
# 9. PREDIKSI MANUAL
# =========================================================
def predict_judol(text):
    cleaned = clean_text(text)
    vec = vectorizer.transform([cleaned])
    pred = model.predict(vec)[0]
    proba = model.predict_proba(vec)[0][1]  # probabilitas kelas "judol"
    return pred, proba

contoh_komentar = [
    "G4COR77 wd cair tiap hari klik bio",
    "Makasih kak videonya bermanfaat banget",
    "Sl0t maxwin malam ini, daftar sekarang!",
    "Request video tentang OOP dong kak"
]

print("\n=== Contoh Prediksi ===")
for c in contoh_komentar:
    label, prob = predict_judol(c)
    status = "JUDOL" if label == 1 else "BUKAN JUDOL"
    print(f"[{status} | prob={prob:.2f}] {c}")

# =========================================================
# 10. INPUT DARI PENGGUNA
# =========================================================
print("\n=== Cek Komentar ===")
print("Masukkan komentar untuk dicek (ketik 'n' untuk keluar)\n")

while True:
    komentar = input("Komentar: ")

    if komentar.strip().lower() == "n":
        print("Selesai.")
        break

    label, prob = predict_judol(komentar)
    status = "JUDOL" if label == 1 else "BUKAN JUDOL"
    print(f"=> [{status} | prob={prob:.2f}]\n")