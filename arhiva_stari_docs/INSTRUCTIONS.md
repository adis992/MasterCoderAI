# 🚀 MasterCoderAI - UPUTE ZA KORIŠTENJE

## ⚠️ VAŽNO - PRIJE PRVOG KORIŠTENJA!

Ako vidiš error `NOT NULL constraint failed: chats.user_id`, to znači da koristiš **STARI TOKEN** iz localStorage!

### ✅ RJEŠENJE:

**OPCIJA 1 - Kroz Browser (NAJBRŽE):**
1. Otvori stranicu: http://172.16.20.104:3000
2. Pritisni **F12** (Developer Tools)
3. Idi na **Console** tab
4. Kucaj: `localStorage.clear()` i pritisni **Enter**
5. **Refresh** stranicu (F5)
6. **LOGIN** ponovo sa `admin` / `admin`

**OPCIJA 2 - Logout i Login:**
1. Klikni **Logout** button
2. **LOGIN** ponovo sa `admin` / `admin`

---

## 📋 KAKO KORISTITI SISTEM:

### 1️⃣ **POKRETANJE SISTEMA:**
```bash
cd /root/MasterCoderAI
./run_all.sh
```

### 2️⃣ **ZAUSTAVLJANJE SISTEMA:**
```bash
cd /root/MasterCoderAI
./stop.sh
```

### 3️⃣ **LOGIN CREDENTIALS:**
- **Admin**: `admin` / `admin`
- **User**: `user` / `user123`

### 4️⃣ **UČITAVANJE MODELA:**
1. Login na http://172.16.20.104:3000
2. Idi na **Models** tab
3. Odaberi model iz dropdown-a
4. Klikni **"🚀 Load to GPU"**
5. **ČEKAJ 1-2 MINUTE** (za 30GB model)
6. Vidjet ćeš "✅ Model loaded!" kad se završi

### 5️⃣ **CHAT SA AI:**
1. Idi na **Chat** tab (nakon što je model učitan)
2. Upiši poruku u input field
3. Klikni **Send** ili pritisni **Enter**
4. AI će odgovoriti!

---

## 🔧 TROUBLESHOOTING:

### ❌ Error: "NOT NULL constraint failed: chats.user_id"
**Uzrok**: Stari token iz localStorage  
**Rješenje**: Očisti localStorage (vidi gore)

### ❌ Error: "No model loaded"
**Uzrok**: Model nije učitan  
**Rješenje**: Idi na Models tab i loadaj model

### ❌ Model se ne učitava
**Uzrok**: Backend nije pokrenut ili nema dovoljno GPU memorije  
**Rješenje**: 
```bash
# Provjeri da li backend radi:
curl http://localhost:8000/health

# Provjeri GPU memoriju:
nvidia-smi

# Restartuj sistem:
cd /root/MasterCoderAI
./stop.sh && ./run_all.sh
```

### ❌ Frontend ne učitava
**Uzrok**: Frontend nije pokrenut  
**Rješenje**:
```bash
cd /root/MasterCoderAI
./run_all.sh
```

---

## 📊 SYSTEM INFO:

- **Backend**: http://172.16.20.104:8000
- **Frontend**: http://172.16.20.104:3000
- **API Docs**: http://172.16.20.104:8000/docs
- **Database**: /root/MasterCoderAI/backend/data.db
- **Models**: /root/MasterCoderAI/modeli/

---

## 🎮 GPU INFO:

Sistem koristi **2x NVIDIA RTX 3090** (ukupno 48GB VRAM) za učitavanje modela.

Provjeri GPU status:
```bash
nvidia-smi
```

---

## 📝 LOGOVI:

**Backend logovi:**
```bash
tail -f /tmp/backend.log
```

**Frontend logovi:**
```bash
tail -f /tmp/frontend.log
```

---

## 🚀 BRZI TEST:

```bash
# 1. Login i dobij token
TOKEN=$(curl -s -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin"}' | jq -r .access_token)

# 2. Provjeri da li je model učitan
curl -s http://localhost:8000/ai/models/current | jq .

# 3. Test chat (ako je model učitan)
curl -X POST http://localhost:8000/ai/chat \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message":"Hello!","save_to_history":true}' | jq .
```

---

**✅ SISTEM JE SPREMAN ZA KORIŠTENJE!**
