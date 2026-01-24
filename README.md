# 🤖 MasterCoderAI

AI Chat System with local GGUF model support, admin panel, and user management.

## Quick Start

```bash
# First time - install everything:
./install.sh

# Run the application:
./run_all.sh
```

## Access

- **Frontend**: http://YOUR_IP:3000
- **Backend API**: http://YOUR_IP:8000

## Login

| Username | Password | Role |
|----------|----------|------|
| admin | admin | Administrator |
| user | user123 | Regular User |

## Features

- 🤖 Local GGUF model loading (llama-cpp-python)
- 💬 Chat with AI (uncensored mode available)
- 👥 User management
- 📊 System monitoring (CPU, RAM, GPU, Disk)
- 🗄️ Database browser
- 🎨 Multiple themes
- ⏱️ Auto-logout after 30 min inactivity

## Structure

```
MasterCoderAI/
├── backend/          # FastAPI backend
│   ├── api/          # API routes
│   ├── db/           # Database config
│   └── data.db       # SQLite database
├── frontend/         # React frontend
│   └── src/
├── modeli/           # GGUF models folder
├── install.sh        # One-time setup
├── run_all.sh        # Start all services
└── stop.sh           # Stop all services
```

## Models

Place your `.gguf` models in the `/modeli/` folder. They will appear in the Models tab.

## Services

After running `install.sh`, services auto-start on reboot:

```bash
systemctl status mastercoderAI-backend
systemctl status mastercoderAI-frontend
```
