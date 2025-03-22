# 🧹 Pembasmi Komentar Judi Online di Youtube

Solusi otomatis untuk membersihkan komentar spam judi di video YouTube Anda dengan mendeteksi pola (kata+angka) dan beberapa kata kunci yang umum digunakan para spammer

![Google Apps Script](https://img.shields.io/badge/Google%20Apps%20Script-02569B?style=for-the-badge&logo=google-script&logoColor=white)
![YouTube API](https://img.shields.io/badge/YouTube%20API-FF0000?style=for-the-badge&logo=youtube&logoColor=white)

## 📜 Daftar Isi
- [Fitur Utama](#-fitur-utama)
- [Prasyarat](#-prasyarat)
- [Cara Install](#%EF%B8%8F-cara-install)
- [Konfigurasi](#%EF%B8%8F-konfigurasi)
- [Cara Pakai](#-cara-pakai)
- [Kustomisasi](#-kustomisasi)
- [Troubleshooting](#-troubleshooting)
- [Berkontribusi](#-berkontribusi)
- [Lisensi](#-lisensi)
- [Disclaimer](#-disclaimer)

## 🌟 Fitur Utama
- **Deteksi Otomatis** pola spam:
  - Kombinasi kata+angka (Contoh: `MANTAP87`, `BOLA123`)
  - Kata kunci judi (`judi online`, `slot`, `bonus deposit`)
- **Menghapus Komentar Otomatis**:
  - Menyembunyikan komentar spam
  - Opsi blokir penulis spam
  - Mode debugging untuk melakukan uji coba
- **Keamanan**:
  - Delay antar request untuk hindari limit API
  - Validasi ID komentar
  - Logging detail

## 📋 Prasyarat
1. Akun Google dengan akses ke [Google Apps Script](https://script.google.com)
2. Video YouTube **milik sendiri**

## ⚙️ Cara Install
1. **Buat Project Baru**:
   - Buka [Google Apps Script](https://script.new)
   - Hapus semua kode default

2. **Aktifkan YouTube API**:
   - Klik `+` di sebelah "Layanan"
   - Cari dan tambahkan **YouTube Data API v3**

3. **Salin Kode**:
   - Copy seluruh kode dari file `Code.gs`
   - Tempel ke editor Apps Script
   
4. **Update Scope**:
   - Buka `appsscript.json`
   - Tambahkan scope berikut:
   ```json
   "oauthScopes": [
     "https://www.googleapis.com/auth/youtube.force-ssl",
     "https://www.googleapis.com/auth/youtube-channel-moderator"
   ]

## 🛠️ Konfigurasi
    Ubah nilai di bagian CONFIG sesuai dengan kebutuhan anda:
    `
    const CONFIG = {
    VIDEO_ID: 'KLcj1cluhP8',    // Ganti dengan ID video target
    MAX_RESULTS: 50,            // Jumlah komentar diproses (1-100)
    DRY_RUN: true,              // True untuk simulasi (tidak eksekusi)
    BAN_AUTHOR: false,          // Blokir penulis spam selamanya
    DELAY: 1500                 // Delay antar aksi (dalam milidetik)
    };`
