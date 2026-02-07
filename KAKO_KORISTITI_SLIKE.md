# 📷 KAKO KORISTITI IMAGE PROCESSING

## 🎯 Brzi Vodič

### 1️⃣ Upload Slike i OCR (Čitanje Teksta)

1. Idi na **Chat** tab
2. Klikni **📷** button pored chat input-a
3. Odaberi sliku sa diska (PNG, JPG, itd.)
4. Slika će se prikazati sa preview-om
5. Napiši pitanje: **"Što piše na slici?"** ili **"Analiziraj ovu sliku"**
6. Klikni 📤 Send
7. AI će:
   - Pročitati tekst sa slike (OCR)
   - Analizirati dimenzije, boje
   - Odgovoriti na tvoje pitanje

**Primjer:**
```
Upload: [slika sa tekstom "STOP"]
Pitanje: "Što piše na ovoj saobraćajnoj oznaci?"
AI: "Na slici vidim tekst: 'STOP'. Ovo je standardna saobraćajna 
     oznaka za obavezno zaustavljanje. Dimenzije slike su 800x600px."
```

### 2️⃣ Generiši Sliku (Image Generation)

1. Klikni **🎨 Generate Image** checkbox
2. Napiši opis slike: **"Create a sunset over mountains"**
3. Klikni 📤 Send
4. AI će opisati sliku koju bi napravio

**Primjer:**
```
Checkbox: ✅ Generate Image
Prompt: "Napravi sliku mačke koja lovi leptira"
AI: "I would create an image showing: A playful orange tabby cat 
     mid-leap, chasing a colorful butterfly in a sunny garden with 
     flowers in the background, rendered in vibrant, photorealistic style."
```

## 🔧 Korisni Tipovi

### Za Najbolji OCR Rezultat:
- ✅ Koristi slike sa jasnim, velikim tekstom
- ✅ Visoki kontrast (npr. crni tekst na bijeloj pozadini)
- ✅ Ravne/frontalne fotografije (bez nagiba)
- ❌ Izbjegavaj zamućene ili niske rezolucije

### OCR Podržava:
- 🇭🇷 Hrvatski jezik
- 🇬🇧 Engleski jezik
- 📝 Štampani tekst
- 🖊️ Neke rukopise (ako su čitljivi)

### Format Slike:
- PNG, JPG, JPEG, BMP, TIFF
- Max 10MB
- Preporučena rezolucija: 1920x1080 ili veća

## 🎨 UI Elementi

| Button/Checkbox | Funkcija |
|-----------------|----------|
| 📷 | Upload sliku za OCR analizu |
| 🎨 Generate Image | Aktivira image generation mod |
| ✖ | Ukloni upload-ovanu sliku |

### Preview Boje:
- **Brown/Smeđa**: Image upload preview
- **Purple/Ljubičasta**: Generate Image checkbox aktivan

## 💡 Primjeri Korištenja

### 1. Skeniranje Dokumenata
```
Upload: [foto fakture]
Pitanje: "Koji je ukupan iznos na ovoj fakturi?"
```

### 2. Prevod Sa Slika
```
Upload: [foto stranog teksta]
Pitanje: "Prevedi tekst sa ove slike na hrvatski"
```

### 3. Analiza Screenshot-a
```
Upload: [screenshot koda sa greškom]
Pitanje: "Što je pogrešno u ovom kodu?"
```

### 4. Kreiranje Umjetnosti
```
Checkbox: ✅ Generate Image
Prompt: "Fantasy dragon breathing fire over medieval castle"
```

## ⚙️ Backend Info

### Tesseract OCR Engine
- **Verzija**: 5.3.4
- **Jezici**: eng (English), hrv (Croatian)
- **Instalacija**: `apt install tesseract-ocr tesseract-ocr-hrv`

### Python Paketi
- `pytesseract` - OCR wrapper
- `Pillow` - Image processing
- `numpy` - Color analysis

## 🚀 Napredne Funkcije (Dolaze Uskoro)

### 🔜 Planirana Poboljšanja:
1. **Stable Diffusion Integration** - Pravi image generation
2. **Multi-Image Upload** - Upload više slika odjednom
3. **Image Editing** - Crop, rotate, filters prije OCR-a
4. **Batch OCR** - Skeniranje PDF-ova sa više stranica
5. **Handwriting Recognition** - Bolji rukopis OCR
6. **Object Detection** - Detekcija objekata na slici (YOLO)

### 🎯 Future API Integracije:
- **DALL-E 3** (OpenAI) - Photorealistic generation
- **Stable Diffusion XL** - Local GPU generation
- **MidJourney API** - Artistic style generation
- **Google Vision API** - Advanced image analysis

## 🐛 Troubleshooting

### OCR Ne Radi?
```bash
# Provjeri da li je tesseract instaliran
tesseract --version

# Ako nije:
sudo apt install tesseract-ocr tesseract-ocr-hrv tesseract-ocr-eng
```

### Python Package Missing?
```bash
# Instaliraj pytesseract
pip3 install --break-system-packages pytesseract

# Restart backend
pkill -f uvicorn
cd /root/MasterCoderAI
nohup uvicorn backend.api.main:app --host 0.0.0.0 --port 8000 --reload &
```

### Preview Ne Pokazuje Sliku?
- Provjeri da li je file size < 10MB
- Provjeri da li je format PNG/JPG
- Otvori browser konzolu (F12) za greške

## 📞 Support

Za dodatnu pomoć:
1. Provjeri `backend.log` za greške
2. Otvori Browser DevTools (F12) → Console
3. Provjeri Network tab za API responses

---

**✅ READY TO USE!**  
Image processing je u potpunosti funkcionalan - probaj odmah! 📷🎨
