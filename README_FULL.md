# 🤖 MasterCoderAI - Full Documentation

**Version:** 2.0.0  
**Release Date:** January 24, 2026  
**Status:** ✅ Production Ready (Minor features pending)

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [Architecture](#architecture)
4. [Installation](#installation)
5. [Usage](#usage)
6. [API Documentation](#api-documentation)
7. [Completed Features](#completed-features)
8. [Pending Features](#pending-features)
9. [Future Roadmap](#future-roadmap)
10. [Troubleshooting](#troubleshooting)

---

## 🎯 Overview

**MasterCoderAI** je potpuno funkcionalna AI chat platforma sa GPU akceleracijom, lokalnim LLM modelima (llama.cpp), i modernim React frontend-om. Sistem podržava multi-user okruženje, admin panel, i real-time monitoring GPU-a.

### Key Highlights:
- ✅ **100% Uncensored** AI responses (DarkIdol Llama 3.1)
- ✅ Multi-GPU support (NVIDIA CUDA)
- ✅ Real-time system monitoring
- ✅ Persistent chat history
- ✅ Role-based access control (Admin/User)
- ✅ Complete REST API
- ✅ Responsive UI (Desktop/Mobile)

---

## 🚀 Features

### ✅ Completed Features

#### Frontend (React)
- [x] Modern responsive UI with dark theme
- [x] Real-time GPU monitoring (3sec refresh)
- [x] System health dashboard
- [x] Chat interface sa:
  - [x] Image upload support
  - [x] Message editing & resending
  - [x] Copy to clipboard (HTTP fallback)
  - [x] Like/Rating system (1-3 stars)
  - [x] Download chat history
  - [x] Auto-scroll to latest message
  - [x] Persistent state (F5 refresh remembers tab & history)
- [x] Admin panel sa:
  - [x] User management (CRUD)
  - [x] Database viewer
  - [x] Model management
  - [x] System settings
  - [x] All chats history sidebar
  - [x] Export all chats funkcija
  - [x] Delete individual chats
- [x] Proper initialization flow (step-by-step loading screen)
- [x] Token expiration handling
- [x] Session persistence (30min inactivity logout)

#### Backend (FastAPI + Python)
- [x] JWT authentication
- [x] Role-based authorization (admin/user)
- [x] SQLite database (async)
- [x] llama-cpp-python integration
- [x] Multi-GPU support
- [x] Model auto-load on startup
- [x] System metrics (CPU, RAM, Disk, GPU)
- [x] Chat history storage
- [x] User settings (temperature, max_tokens, etc.)
- [x] CORS enabled (LAN access)
- [x] Uncensored mode (default)
- [x] Web search integration (optional)

#### Models
- [x] DarkIdol Llama 3.1 8B Uncensored (Q8_0.gguf - 8.5GB)
- [x] Auto GPU offload (100% layers)
- [x] Streaming support
- [x] Context window: 8192 tokens

#### Infrastructure
- [x] Shell scripts za easy deployment
- [x] Auto-install dependencies
- [x] Background process management
- [x] Logging sistema
- [x] Health checks

---

## 🏗️ Architecture

```
MasterCoderAI/
├── backend/
│   ├── api/
│   │   ├── main.py          # FastAPI app
│   │   ├── auth.py          # JWT authentication
│   │   ├── ai.py            # LLM integration
│   │   ├── admin.py         # Admin endpoints
│   │   ├── user.py          # User endpoints
│   │   ├── system.py        # System monitoring
│   │   └── models.py        # SQLAlchemy models
│   └── db/
│       ├── database.py      # Database connection
│       └── models.py        # Database schema
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   │   ├── Dashboard.js # Main app
│   │   │   └── Login.js     # Login page
│   │   ├── App.js
│   │   └── index.js
│   └── build/               # Production build
├── modeli/
│   └── DarkIdol-Llama-3.1-8B-Instruct-1.2-Uncensored.Q8_0.gguf
├── testiranje/              # Test scripts (isolated)
├── run_all.sh               # Main startup script
├── run.sh                   # Backend only
├── start.sh                 # Alternative startup
└── stop.sh                  # Shutdown script
```

---

## 📦 Installation

### Prerequisites
- Ubuntu/Debian Linux
- Python 3.10+
- Node.js 16+
- NVIDIA GPU (optional but recommended)
- CUDA Toolkit 11.8+ (for GPU)

### Quick Start

```bash
# 1. Clone repository
git clone <repo-url>
cd MasterCoderAI

# 2. Run installation
chmod +x run_all.sh
./run_all.sh

# 3. Access aplikacije
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Manual Installation

```bash
# Backend
cd backend
pip install -r requirements.txt

# Frontend
cd frontend
npm install
npm run build

# Start services
cd ..
./run.sh  # Backend
# Frontend is served from build/
```

---

## 💻 Usage

### Default Credentials
- **Admin:** `admin` / `admin123`
- **User:** `user` / `user123`

### Admin Features
1. **Dashboard** - System stats, GPU monitoring
2. **Models** - Load/unload AI models
3. **Users** - Add/edit/delete users
4. **Database** - Direct database access
5. **System** - Settings & configuration
6. **Chat History** - View/delete/export all chats

### User Features
1. **Chat** - Talk to AI
2. **Settings** - Customize AI parameters

### Model Loading
1. Go to **Models** tab
2. Select model from dropdown
3. Click **Load to GPU**
4. Wait 1-2 minutes for initialization
5. Green status = ready to chat!

---

## 📡 API Documentation

### Authentication Endpoints

#### POST `/auth/login`
Login user and get JWT token.

**Request:**
```json
{
  "username": "admin",
  "password": "admin123"
}
```

**Response:**
```json
{
  "access_token": "eyJ...",
  "token_type": "bearer"
}
```

### AI Endpoints

#### POST `/ai/chat`
Send message to AI and get response.

**Headers:**
```
Authorization: Bearer <token>
```

**Request:**
```json
{
  "message": "Hello AI!",
  "save_to_history": true
}
```

**Response:**
```json
{
  "message": "Hello AI!",
  "response": "Hello! How can I help you today?",
  "model_name": "DarkIdol-Llama-3.1...",
  "saved": true,
  "uncensored": true
}
```

#### GET `/ai/models`
List all available models.

#### POST `/ai/models/load`
Load model to GPU.

#### GET `/ai/gpu`
Get GPU status and metrics.

### Admin Endpoints

#### GET `/admin/users`
List all users (admin only).

#### GET `/admin/chats`
Get all chat history (admin only).

#### DELETE `/admin/chats/{chat_id}`
Delete specific chat (admin only).

### System Endpoints

#### GET `/system/health`
System health check.

#### GET `/system/settings`
Get system settings.

Full API docs: `http://localhost:8000/docs`

---

## ✅ Completed Features (v2.0.0)

### Core Functionality
- ✅ Multi-user authentication
- ✅ Admin panel
- ✅ Model loading to GPU
- ✅ Real-time chat with AI
- ✅ Chat history persistence
- ✅ GPU monitoring
- ✅ System health monitoring

### UI/UX
- ✅ Responsive design
- ✅ Dark theme
- ✅ Loading screens
- ✅ Error handling
- ✅ Clipboard support (HTTP fallback)
- ✅ Auto-scroll chat
- ✅ Persistent state (F5)
- ✅ Like/rating system

### Admin Tools
- ✅ User management
- ✅ Database viewer
- ✅ Chat history sidebar
- ✅ Export chats
- ✅ Delete chats
- ✅ System settings

### Backend
- ✅ JWT authentication
- ✅ Database migrations
- ✅ Model auto-load
- ✅ CORS support
- ✅ Streaming responses
- ✅ Error logging

---

## ⏳ Pending Features

### Minor Improvements Needed:
- [ ] Chat rename functionality (sidebar)
- [ ] Background initialization (no panel refresh)
- [ ] Web search toggle UI
- [ ] Prompt mode selector UI
- [ ] Theme selection (currently dark only)
- [ ] Mobile menu improvements
- [ ] Image upload in chat (backend ready, UI needs polish)

### Known Issues:
- ⚠️ Clipboard API requires HTTPS (fallback implemented)
- ⚠️ Initialization sometimes refreshes panel (cosmetic)
- ⚠️ Large chat histories slow down UI (need pagination)

---

## 🔮 Future Roadmap

### v2.1 (Next Release)
- [ ] Chat rename functionality
- [ ] Background initialization fix
- [ ] Pagination for chat history
- [ ] Better mobile responsiveness
- [ ] Theme switcher (light/dark)
- [ ] User profile pages
- [ ] Password change functionality

### v2.2 (Planned)
- [ ] Multi-model chat (compare responses)
- [ ] Voice input/output
- [ ] Document upload & RAG
- [ ] Custom prompt templates
- [ ] API rate limiting
- [ ] Webhooks support

### v3.0 (Future)
- [ ] Multi-language support
- [ ] Plugin system
- [ ] Docker deployment
- [ ] Kubernetes support
- [ ] Redis caching
- [ ] PostgreSQL migration
- [ ] Real-time collaboration
- [ ] Mobile app (React Native)

---

## 🐛 Troubleshooting

### Model won't load
```bash
# Check GPU availability
nvidia-smi

# Check model file
ls -lh /root/MasterCoderAI/modeli/

# Check backend logs
tail -f /tmp/backend.log
```

### Chat returns "Network Error"
```bash
# Check if backend is running
curl http://localhost:8000/health

# Restart backend
./stop.sh && ./run.sh
```

### Login fails
```bash
# Reset admin password
cd backend
python3 -c "
from werkzeug.security import generate_password_hash
import sqlite3
conn = sqlite3.connect('data.db')
hash = generate_password_hash('admin123')
conn.execute('UPDATE users SET hashed_password=? WHERE username=\"admin\"', (hash,))
conn.commit()
print('Password reset!')
"
```

### GPU not detected
```bash
# Install CUDA
sudo apt install nvidia-cuda-toolkit

# Reinstall llama-cpp-python with GPU
pip uninstall llama-cpp-python -y
CMAKE_ARGS="-DLLAMA_CUBLAS=on" pip install llama-cpp-python --no-cache-dir
```

---

## 📄 License

Proprietary - All Rights Reserved

---

## 👥 Credits

- **LLM Engine:** llama.cpp
- **Model:** DarkIdol Llama 3.1 Uncensored
- **Frontend:** React 18
- **Backend:** FastAPI
- **Database:** SQLite (async)

---

## 📞 Support

For issues or questions, check logs:
- Backend: `/tmp/backend.log`
- Browser: Console (F12)
- System: `/var/log/syslog`

---

**Last Updated:** January 24, 2026  
**Maintained by:** MasterCoderAI Team
