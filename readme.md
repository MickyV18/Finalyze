# Finalyze

Developed by:

- Name: Micky Valentino
- NIM: 18222093
- Course: II3160 Teknologi Sistem Terintegrasi

## Overview

Finalyze adalah website pengelolaan uang yang dirancang untuk membantu pengguna dalam manajemen keuangan pribadi. Website ini menyediakan layanan terpadu dengan berbagai fitur utama seperti autentikasi pengguna, pencatatan keuangan, dan deteksi anomali berbasis AI.

## Core Features

### 1. Authentication (Google OAuth)

- Login menggunakan akun Google
- Integrasi dengan Supabase untuk manajemen pengguna
- Keamanan data pengguna yang terjamin
- Session management yang efisien

### 2. Pencatatan Keuangan

- Input pengeluaran dengan detail kategori
- Pencatatan tanggal dan deskripsi transaksi
- Penyimpanan riwayat transaksi
- Visualisasi data pengeluaran
- Manajemen kategori pengeluaran

### 3. AI Anomaly Detection

- Deteksi anomali pengeluaran menggunakan machine learning
- Analisis pola pengeluaran berdasarkan data historis
- Peringatan untuk transaksi yang mencurigakan
- Model berbasis Isolation Forest
- Pembelajaran dari data default dan data historis pengguna

## Tech Stack

### Backend

- **FastAPI**: Framework web Python untuk backend
- **Supabase**: Database dan autentikasi
- **Python dotenv**: Manajemen environment variables

### Frontend

- **HTML/CSS**: Struktur dan styling website
- **Jinja2**: Template engine untuk rendering halaman

### Machine Learning

- **scikit-learn**: Library untuk implementasi Isolation Forest
- **Pandas**: Manipulasi dan analisis data

### Authentication

- **Google OAuth 2.0**: Sistem autentikasi pengguna

### Development & Deployment

- **Docker**: Kontainerisasi aplikasi
- **Railway**: Platform deployment
- **Git**: Version control

## API Documentation

Dokumentasi API lengkap tersedia di:

- `/docs` - Swagger UI documentation
- `/redoc` - ReDoc documentation
  
## Endpoint

### Halaman Beranda
- **URL**: `/`
- **Metode**: `GET`
- **Respons**:
  - **200**: Mengembalikan halaman beranda dalam format `text/html`

### Halaman Dasbor
- **URL**: `/dashboard`
- **Metode**: `GET`
- **Respons**:
  - **200**: Mengembalikan halaman dasbor dalam format `text/html`

### Dasbor Anomali
- **URL**: `/anomaly-dashboard`
- **Metode**: `GET`
- **Respons**:
  - **200**: Mengembalikan halaman dasbor anomali dalam format `text/html`

### Login dengan Google
- **URL**: `/auth/login`
- **Metode**: `GET`
- **Respons**:
  - **200**: Mengembalikan data JSON untuk proses login Google

### Callback
- **URL**: `/auth/callback`
- **Metode**: `GET`
- **Parameter Query**:
  - `code` (string, wajib): Kode otorisasi
- **Respons**:
  - **200**: Mengembalikan respons JSON
  - **422**: Error validasi dengan pesan error terperinci

### Halaman Login
- **URL**: `/auth/login-page`
- **Metode**: `GET`
- **Respons**:
  - **200**: Mengembalikan halaman login dalam format `text/html`

### Dasbor Terautentikasi
- **URL**: `/auth/dashboard`
- **Metode**: `GET`
- **Parameter Query**:
  - `user_name` (string, opsional, default: "User"): Nama pengguna yang ditampilkan di dasbor
- **Respons**:
  - **200**: Mengembalikan halaman dasbor dalam format `text/html`
  - **422**: Error validasi dengan pesan error terperinci

### Logout
- **URL**: `/auth/logout`
- **Metode**: `GET`
- **Respons**:
  - **200**: Mengembalikan halaman logout dalam format `text/html`

### Deteksi Anomali
- **URL**: `/api/anomaly/detect`
- **Metode**: `POST`
- **Body Request**:
  ```json
  {
    "amount": 1,
    "date": "4419-18-06",
    "category": "lainnya",
    "description": "string",
    "user_id": "string"
  }
  ```
- **Respons**:
  - **200**: Mengembalikan respons JSON untuk deteksi yang berhasil
  - **422**: Error validasi dengan pesan error terperinci

### Mendapatkan Riwayat Anomali
- **URL**: `/api/anomaly/history/{user_id}`
- **Metode**: `GET`
- **Parameter Path**:
  - `user_id` (string, wajib): ID pengguna untuk mengambil riwayat
- **Respons**:
  - **200**: Mengembalikan respons JSON dengan riwayat anomali
  - **422**: Error validasi dengan pesan error terperinci

### Halaman Anomali
- **URL**: `/anomaly`
- **Metode**: `GET`
- **Respons**:
  - **200**: Mengembalikan informasi anomali dalam format JSON

## Skema

### HTTPValidationError
- **Field**:
  - `detail` (array objek):
    - `loc` (array string | integer): Lokasi error
    - `msg` (string): Pesan error
    - `type` (string): Tipe error

### Transaction
- **Field**:
  - `amount` (angka, wajib): Harus lebih besar dari 0
  - `date` (string, wajib): Harus sesuai format `YYYY-MM-DD`
  - `category` (string, wajib): Harus sesuai kategori yang ditentukan (contoh: makanan berat, minuman, transportasi, lainnya)
  - `description` (string, wajib): Harus antara 1 dan 255 karakter
  - `user_id` (string, wajib): Harus memiliki minimal 1 karakter

### ValidationError
- **Field**:
  - `loc` (array string | integer): Lokasi error
  - `msg` (string): Pesan error
  - `type` (string): Tipe error

## Penanganan Error
API mengembalikan kode status HTTP standar untuk menunjukkan keberhasilan atau kegagalan request:
- **200**: Request berhasil
- **422**: Error validasi dengan detail tentang parameter request yang tidak sesuai

## Contact

For any questions or feedback, please contact the maintainer at [18222093@std.stei.itb.ac.id].

## Links

- Website: [Website Finalyze](https://finalyze.up.railway.app/)
- GitHub: [Github Finalyze](https://github.com/MickyV18/Finalyze)
- Document: [Document Finalyze](https://docs.google.com/document/d/14WK7uafgyp0ZMGCIB1slm0hBcFGBWBIP3KtALS4k7gM/edit?usp=sharing)
