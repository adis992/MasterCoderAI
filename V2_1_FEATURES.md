# 🚀 MasterCoderAI v2.1 - SVE NOVE FUNKCIJE

## ✅ ŠTA JE DODANO

### 1. 🧠 DeepLearning Mode
**Lokacija**: Settings Tab → User Settings

3 slider opcije:
- **Intensity** (0.0 - 1.0) - Dubina analize
- **Context** (0.0 - 1.0) - Koliko široko AI razmišlja
- **Memory** (0.0 - 1.0) - Korištenje conversation historije

**Kako radi**: Kad je Intensity > 0.5, AI automatski prelazi u DeepLearning mod i analizira dublje.

---

### 2. 🎭 Opinion & Judgment Mode
**Lokacija**: Settings Tab → User Settings

3 slider opcije:
- **Confidence** (0.0 - 1.0) - Sigurnost u mišljenju
- **Creativity** (0.0 - 1.0) - Kreativnost u pristupu
- **Critical Thinking** (0.0 - 1.0) - Kritičko razmišljanje

**Kako radi**: Kad je Confidence > 0.5, AI daje vlastito mišljenje i subjektivnu procjenu.

---

### 3. 💻 VSCode Web Integration
**Lokacija**: Settings Tab → VSCode Integration

- **Auto Open** - Automatski prikaži VSCode dugme
- **Permissions** - Kontrola pristupa

**Kako koristiti**:
1. Omogući "Auto Open"
2. Spomeni "create project" ili "novi projekt" u chatu
3. Klikni **🚀 Open VSCode** dugme
4. Otvara `vscode.dev` u novom tabu

**Napomena**: Otvara VSCode Web (browser verzija), NE desktop aplikaciju!

---

### 4. 🌐 Smart Web Search
**Lokacija**: Settings Tab → Web Search Integration

- **Enable Web Search** - Omogući pristup internetu
- **Threshold** (1-10) - Koliko ključnih riječi pokreće search

**Keyword lista**: "latest, current, price, today, now, real-time, news, weather, stock, crypto, exchange rate, score, trenutno, cijena, danas, vrijeme, vijesti"

**Kako radi**:
- AI detektuje da li poruka sadrži ključne riječi
- Ako da, automatski traži po webu prije odgovora
- Pokazuje 🌐 indicator tokom pretrage

---

### 5. 🌍 Language Forcing
**Lokacija**: Chat Tab → Language Selector (iznad inputa)

Opcije:
- **Auto-detect** (default)
- 🇭🇷 Force Croatian
- 🇬🇧 Force English
- 🇩🇪 Force German
- 🇪🇸 Force Spanish

**Kako radi**: Dodaje `[IMPORTANT: Respond ONLY in X language]` na kraj poruke.

---

### 6. 📷 Image Upload (OCR)
**Lokacija**: Chat Tab → 📷 button

**Funkcionalnost**:
- Upload slike sa tekstom
- Tesseract OCR čita tekst
- AI dobija text i odgovara

**Primjer**:
1. Screenshot koda → upload → "Explain this"
2. Meme → upload → "What's the joke?"
3. Document → upload → "Summarize"

---

### 7. 🎨 Image Generation Toggle
**Lokacija**: Chat Tab → checkbox "🎨 Generate Image"

**Status**: Checkbox radi, backend spreman, ali fali:
- Stable Diffusion integracija
- DALL-E API

**Trenutno**: AI opisuje kako slika treba izgledati (tekstualno).

---

### 8. 💭 Thinking Phase Visualization
**Svaka poruka ima 1.7s "thinking" animacija**:

```
🧠 AI is thinking...
   Analyzing your message...
```

Prikazuje se prije svakog odgovora, daje feedback da AI radi.

---

### 9. 🎨 Responsive Design Improvements

**Breakpoints**:
- **Desktop** (1200px+): Full sidebar, normal font
- **Tablet** (768px-1200px): 30% manji font, sidebar vidljiv
- **Mobile** (<768px): Hamburger menu, 30% manji font

**Font Reduction**: SVE fontove smanjeno za 30% (`font-size: 70%`)

**Hamburger Menu**:
- Klikni **☰** na mobilnom
- Sidebar izlazi s lijeva
- Klikni **✖** za zatvaranje

---

## 🗄️ Database Changes

**Nova polja u `user_settings` tabeli**:
```sql
deeplearning_intensity FLOAT DEFAULT 0.8
deeplearning_context FLOAT DEFAULT 1.0
deeplearning_memory FLOAT DEFAULT 0.9
opinion_confidence FLOAT DEFAULT 0.7
opinion_creativity FLOAT DEFAULT 0.8
opinion_critical_thinking FLOAT DEFAULT 0.9
vscode_auto_open BOOLEAN DEFAULT 0
vscode_permissions TEXT DEFAULT 'limited'
auto_web_search BOOLEAN DEFAULT 1
web_search_threshold INTEGER DEFAULT 3
```

**Migracija**: Automatska pri startupu ako fale kolone.

---

## 📦 Nove Dependency

### System Packages
```bash
tesseract-ocr  # OCR engine
```

### Python Packages
```bash
pillow>=10.0.0      # Image processing
pytesseract>=0.3.10 # OCR wrapper
numpy>=1.24.0       # Array operations
```

**Install**: Sve u `install.sh` i `requirements.txt`

---

## 🔧 Troubleshooting

### Problem: "Network Error - Cannot reach backend"
**Fix**:
```bash
# 1. Kill old processes
lsof -ti:8000 | xargs kill -9

# 2. Restart backend
cd /root/MasterCoderAI/backend
/root/MasterCoderAI/.venv/bin/python -m uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```

### Problem: CORS Error
**Fix**: Već riješeno - `allow_origins=["*"]` u `main.py`

### Problem: Image upload ne radi
**Fix**:
```bash
# Install Tesseract
apt-get install -y tesseract-ocr

# Install Python packages
pip3 install pillow pytesseract numpy
```

### Problem: Frontend warnings
**Fix**: Ignorisati - to su unused variables, NE utiču na funkcionalnost.

---

## 🎯 Quick Test Commands

```bash
# 1. Check backend
curl http://localhost:8000/docs

# 2. Check if model loaded
curl http://localhost:8000/ai/status

# 3. Test chat endpoint
curl -X POST http://localhost:8000/ai/chat \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message":"test"}'

# 4. Frontend rebuild
cd /root/MasterCoderAI/frontend
npm run build

# 5. Backend restart
cd /root/MasterCoderAI/backend
/root/MasterCoderAI/.venv/bin/python -m uvicorn api.main:app --host 0.0.0.0 --port 8000
```

---

## 📊 File Changes Summary

**Modified Files**:
- `frontend/src/pages/Dashboard.js` (+300 lines)
- `frontend/src/Dashboard.css` (+150 lines responsive)
- `backend/api/models.py` (+10 columns)
- `backend/api/user.py` (+10 fields)
- `backend/api/ai.py` (+150 lines image processing)
- `install.sh` (+3 packages)
- `requirements.txt` (+3 packages)

**New Files**:
- `IMAGE_UPLOAD_GUIDE.md`
- `V2_1_FEATURES.md` (this file)

---

## 🚀 Next Steps

1. ✅ Test image upload sa pravom slikom
2. ✅ Provjeri da svi settings save to database
3. ⏳ Dodaj Stable Diffusion za pravu image generation
4. ⏳ Optimizuj OCR accuracy (treniranje)
5. ⏳ Dodaj image cache za brže učitavanje

---

**Version**: v2.1  
**Date**: January 25, 2026  
**Status**: ✅ Production Ready (except real image generation)
