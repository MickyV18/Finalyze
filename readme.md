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

## Endpoints

### Landing Page

- **URL**: `/`
- **Method**: `GET`
- **Response**:
  - **200**: Returns the landing page in `text/html` format.

### Dashboard Page

- **URL**: `/dashboard`
- **Method**: `GET`
- **Response**:
  - **200**: Returns the dashboard page in `text/html` format.

### Anomaly Dashboard

- **URL**: `/anomaly-dashboard`
- **Method**: `GET`
- **Response**:
  - **200**: Returns the anomaly dashboard page in `text/html` format.

### Login with Google

- **URL**: `/auth/login`
- **Method**: `GET`
- **Response**:
  - **200**: Returns JSON data for the Google login process.

### Callback

- **URL**: `/auth/callback`
- **Method**: `GET`
- **Query Parameters**:
  - `code` (string, required): Authorization code.
- **Response**:
  - **200**: Returns a JSON response.
  - **422**: Validation error with detailed error messages.

### Login Page

- **URL**: `/auth/login-page`
- **Method**: `GET`
- **Response**:
  - **200**: Returns the login page in `text/html` format.

### Authenticated Dashboard

- **URL**: `/auth/dashboard`
- **Method**: `GET`
- **Query Parameters**:
  - `user_name` (string, optional, default: "User"): User name to display on the dashboard.
- **Response**:
  - **200**: Returns the dashboard page in `text/html` format.
  - **422**: Validation error with detailed error messages.

### Logout

- **URL**: `/auth/logout`
- **Method**: `GET`
- **Response**:
  - **200**: Returns the logout page in `text/html` format.

### Detect Anomaly

- **URL**: `/api/anomaly/detect`
- **Method**: `POST`
- **Request Body**:
  ```json
  {
    "amount": 1,
    "date": "4419-18-06",
    "category": "lainnya",
    "description": "string",
    "user_id": "string"
  }
  ```
- **Response**:
  - **200**: Returns JSON response for a successful detection.
  - **422**: Validation error with detailed error messages.

### Get Anomaly History

- **URL**: `/api/anomaly/history/{user_id}`
- **Method**: `GET`
- **Path Parameters**:
  - `user_id` (string, required): User ID for fetching history.
- **Response**:
  - **200**: Returns JSON response with anomaly history.
  - **422**: Validation error with detailed error messages.

### Anomaly Page

- **URL**: `/anomaly`
- **Method**: `GET`
- **Response**:
  - **200**: Returns anomaly information in JSON format.

## Schemas

### HTTPValidationError

- **Fields**:
  - `detail` (array of objects):
    - `loc` (array of string | integer): Location of the error.
    - `msg` (string): Error message.
    - `type` (string): Type of the error.

### Transaction

- **Fields**:
  - `amount` (number, required): Must be greater than 0.
  - `date` (string, required): Must match format `YYYY-MM-DD`.
  - `category` (string, required): Must match predefined categories (e.g., makanan berat, minuman, transportasi, lainnya).
  - `description` (string, required): Must be between 1 and 255 characters.
  - `user_id` (string, required): Must have at least 1 character.

### ValidationError

- **Fields**:
  - `loc` (array of string | integer): Location of the error.
  - `msg` (string): Error message.
  - `type` (string): Type of the error.

## Error Handling

The API returns standard HTTP status codes to indicate success or failure of requests:

- **200**: Request was successful.
- **422**: Validation error with details about the incorrect request parameters.

## Contact

For any questions or feedback, please contact the maintainer at [email@example.com].

## Links

- Website: [Website Finalyze](https://finalyze.up.railway.app/)
- GitHub: [Github Finalyze](https://github.com/MickyV18/Finalyze)
- Document: [Document Finalyze](https://docs.google.com/document/d/14WK7uafgyp0ZMGCIB1slm0hBcFGBWBIP3KtALS4k7gM/edit?usp=sharing)
