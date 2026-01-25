# 🤖 MasterCoderAI

Local AI Chat aplikacija sa potpunim GPU offloadom za GGUF modele.

## ✨ Funkcionalnosti

### 💬 AI Chat Panel
- Real-time chat sa lokalnim AI modelima
- Web search integracija (DuckDuckGo)
- Uncensored mode toggle
- Force language (Auto/English/Croatian)
- Image upload support
- Master prompts (Master Coder, Creative Writer, Data Analyst...)
- Chat history sa rating sistemom (⭐)
- Edit/Delete/Regenerate poruke
- Copy to clipboard
- Clear chat funkcija

### 🎛️ Admin Dashboard
- System status monitoring (CPU, RAM, Disk)
- Real-time GPU monitoring (VRAM, Temperature, Load)
- Model management (Load/Unload)
- Multi-GPU support (distribucija layera)
- External drive model support (/mnt/12T/models)

### 👥 User Management
- Admin/User role sistem
- JWT authentication
- User chat history
- Per-user settings

### ⚙️ System Settings
- Chat enable/disable
- Model auto-load on startup
- Max message length
- Rate limiting
- Maintenance mode
- Dark web search toggle
- Uncensored default toggle

### 📊 Database Panel (Admin)
- View all tables (users, chats, settings)
- Direct database inspection
- Export data

## 🚀 Quick Start

```bash
# Kloniraj repo
git clone https://github.com/adis992/MasterCoderAI.git
cd MasterCoderAI

# Instaliraj sve
chmod +x install.sh
./install.sh

# Pokreni
./run_all.sh
```

## 📁 Struktura Projekta

```
MasterCoderAI/
├── backend/           # FastAPI backend
│   ├── api/           # API endpoints
│   │   ├── main.py    # Main app entry
│   │   ├── ai.py      # AI/Chat endpoints
│   │   ├── auth.py    # Authentication
│   │   ├── admin.py   # Admin endpoints
│   │   ├── user.py    # User endpoints
│   │   └── system.py  # System endpoints
│   └── db/            # Database models
├── frontend/          # React frontend
│   ├── src/
│   │   ├── pages/     # Dashboard, Login
│   │   └── components/
│   └── build/         # Production build
├── modeli/            # Local GGUF models
├── testiranje/        # Test scripts
└── arhiva_stari_docs/ # Old documentation
```

## 🔧 Konfiguracija

### Model Directories
Modeli se traže u:
- `/root/MasterCoderAI/modeli/` - Lokalni modeli
- `/mnt/12T/models/` - Eksterni disk modeli

### Portovi
- Backend API: `http://localhost:8000`
- Frontend: `http://localhost:3000`

### Default Login
- Username: `admin`
- Password: `admin`

## 🖥️ Hardware Requirements

- **GPU**: NVIDIA sa CUDA support (RTX 3090 preporučeno)
- **VRAM**: Ovisno o modelu (8GB-48GB)
- **RAM**: 16GB+ preporučeno
- **Storage**: SSD za modele

## 📦 Dependencies

### Python
- FastAPI, Uvicorn
- llama-cpp-python (CUDA)
- python-jose, passlib
- databases, aiosqlite
- GPUtil, psutil

### Frontend
- React 18
- Axios
- CSS modules

## 🛠️ Scripts

| Script | Opis |
|--------|------|
| `./run_all.sh` | Pokreni backend + frontend |
| `./start.sh` | Start services |
| `./stop.sh` | Stop services |
| `./install.sh` | Full installation |

## 📝 API Endpoints

### Auth
- `POST /auth/login` - Login
- `POST /auth/register` - Register

### AI
- `GET /ai/models` - List models
- `POST /ai/models/load` - Load model
- `GET /ai/models/current` - Current model status
- `POST /ai/chat` - Send chat message
- `GET /ai/gpu` - GPU info

### User
- `GET /user/chats` - User chat history
- `GET /user/settings` - User settings

### Admin
- `GET /admin/users` - All users
- `GET /admin/chats` - All chats
- `DELETE /admin/chats/{id}` - Delete chat

### System
- `GET /system/health` - Health check
- `GET /system/settings` - System settings

## 🐛 Troubleshooting

### Model ne radi
```bash
# Provjeri GPU
nvidia-smi

# Provjeri llama-cpp CUDA support
python3 -c "from llama_cpp import Llama; print('OK')"
```

### Frontend ne radi
```bash
cd frontend
npm run build
```

### Backend error
```bash
tail -f /tmp/backend.log
```

## 📄 License

MIT License

## 👤 Author

adis992
