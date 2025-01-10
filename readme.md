# 💰 Finalyze - Your Personal Finance Companion
![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/Python-FastAPI-green)
![License](https://img.shields.io/badge/license-MIT-orange)
> A smart financial management platform powered by AI to help you make better financial decisions.

Developed by **Micky Valentino** (18222093)  
*II3160 Teknologi Sistem Terintegrasi*

## 🔗 Quick Links
- 🌐 [Live Website](https://finalyze.up.railway.app/)
- 💻 [GitHub Repository](https://github.com/MickyV18/Finalyze)
- 📄 [Document](https://drive.google.com/file/d/10UH2RBS_3tc13GL42URFYEDE4vYC6dNQ/view?usp=sharing)

## 🌟 Overview
Finalyze is your one-stop solution for personal finance management. Combining cutting-edge AI technology with user-friendly interfaces, it helps you track expenses, detect unusual spending patterns, and maintain better control over your finances.

This website is integrated with [Service Chatbot](https://spotify-bot.azurewebsites.net/) created by Jonathan Wiguna / 18222019

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

### 🎵 Spotify Integration
- **Music-Finance Synergy**
  - Real-time integration with Spotify Bot
  - Mood-based playlist recommendations based on financial status
  - Automated playlist generation for different financial activities
  - Seamless connection with Spotify's API

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

### 🐳 Containerization
```
Docker       → Application containerization
Docker Compose → Multi-container orchestration
Docker Hub    → Container registry
```

### ⚙️ DevOps
```
Docker   → Application containerization
Railway  → Cloud deployment platform
Git      → Version control
Azure    → Spotify Bot hosting
```

## 📚 API Documentation
To use the Finalyze service, contact the Finalyze service owner and send the service link for permission. Then read the API Documentation to see the endpoint you want to go to and create code that points to the Finalyze service endpoint path.

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

#### 🎵 Spotify Integration
| Endpoint                    | Method | Description                           |
| --------------------------- | ------ | ------------------------------------- |
| `/api/spotify/connect`      | GET    | Initialize Spotify connection         |
| `/api/spotify/recommendations`| GET   | Get mood-based playlist suggestions  |

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
