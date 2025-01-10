# 💰 Finalyze - Your Personal Finance Companion

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/Python-FastAPI-green)
![License](https://img.shields.io/badge/license-MIT-orange)

> A smart financial management platform powered by AI to help you make better financial decisions.

Developed by **Micky Valentino** (18222093)  
_II3160 Teknologi Sistem Terintegrasi_

## 🔗 Quick Links

- 🌐 [Live Website](https://finalyze.up.railway.app/)
- 💻 [GitHub Repository](https://github.com/MickyV18/Finalyze)
- 📄 [Documentation](https://docs.google.com/document/d/14WK7uafgyp0ZMGCIB1slm0hBcFGBWBIP3KtALS4k7gM/edit?usp=sharing)

## 🌟 Overview

Finalyze is your one-stop solution for personal finance management. Combining cutting-edge AI technology with user-friendly interfaces, it helps you track expenses, detect unusual spending patterns, and maintain better control over your finances.

## 🚀 Core Features

### 🔐 Secure Authentication

- **Google OAuth Integration**
  - Seamless login with your Google account
  - Robust security powered by Supabase
  - Efficient session management
  - Protected user data

### 💳 Smart Financial Tracking

- **Comprehensive Transaction Management**
  - Categorized expense tracking
  - Detailed transaction history
  - Interactive data visualizations
  - Flexible category management

### 🤖 AI-Powered Anomaly Detection

- **Intelligent Spending Analysis**
  - Machine learning-based unusual transaction detection
  - Historical spending pattern analysis
  - Smart alerts for suspicious activities
  - Isolation Forest algorithm implementation
  - Adaptive learning from user patterns

## 🛠️ Tech Stack

### 🔧 Backend Architecture

```
FastAPI     → Lightning-fast web framework
Supabase    → Database & Authentication
Python      → Core programming language
```

### 🎨 Frontend Technologies

```
HTML/CSS    → Structure & styling
Jinja2      → Template rendering
```

### 🧠 Machine Learning Stack

```
scikit-learn → Isolation Forest implementation
Pandas       → Data processing & analysis
```

### 🔒 Security

```
Google OAuth 2.0 → Secure user authentication
```

### ⚙️ DevOps

```
Docker   → Application containerization
Railway  → Cloud deployment platform
Git      → Version control
```

## 📚 API Documentation

### 🔍 Interactive Documentation

- Swagger UI: [Swagger](https://finalyze.up.railway.app/docs)
- ReDoc: [ReDoc](https://finalyze.up.railway.app/redoc)

### 🛣️ Key Endpoints

#### 📱 User Interface

| Endpoint             | Method | Description                 |
| -------------------- | ------ | --------------------------- |
| `/`                  | GET    | Home page                   |
| `/dashboard`         | GET    | Main dashboard              |
| `/anomaly-dashboard` | GET    | Anomaly detection dashboard |

#### 🔐 Authentication

| Endpoint         | Method | Description             |
| ---------------- | ------ | ----------------------- |
| `/auth/login`    | GET    | Google login initiation |
| `/auth/callback` | GET    | OAuth callback handling |
| `/auth/logout`   | GET    | User logout             |

#### 🤖 Anomaly Detection

| Endpoint                         | Method | Description                       |
| -------------------------------- | ------ | --------------------------------- |
| `/api/anomaly/detect`            | POST   | Analyze transaction for anomalies |
| `/api/anomaly/history/{user_id}` | GET    | Retrieve anomaly history          |

## 📊 Data Schemas

### 📝 Transaction Schema

```json
{
  "amount": "number (> 0)",
  "date": "YYYY-MM-DD",
  "category": "string (predefined categories)",
  "description": "string (1-255 chars)",
  "user_id": "string (min 1 char)"
}
```

## 🚨 Error Handling

- **200**: Success
- **422**: Validation Error (with detailed feedback)

## 📞 Contact

Got questions? Reach out!  
📧 [18222093@std.stei.itb.ac.id](mailto:18222093@std.stei.itb.ac.id)
