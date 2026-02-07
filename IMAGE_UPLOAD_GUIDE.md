# 📷 Image Upload & Generation - Quick Guide

## ✅ What's Working

### 1. **Image Upload for OCR (Text Recognition)**
- Click **📷 button** next to chat input
- Select any image with text
- AI will read the text using Tesseract OCR
- Works with: screenshots, documents, memes, photos with text

### 2. **Image Generation Toggle**
- **🎨 Generate Image** checkbox next to upload button
- Check it when you want AI to describe/create an image
- Currently: AI describes what image should look like
- Future: Integration with DALL-E or Stable Diffusion

### 3. **Image Preview**
- After uploading, see preview above chat input
- Shows thumbnail + "AI će analizirati sliku i pročitati tekst"
- Click **✖** to remove image before sending

---

## 🛠️ Technical Stack

### Backend
- **OCR Engine**: Tesseract OCR (`tesseract-ocr` package)
- **Python Libraries**:
  - `pytesseract` - OCR wrapper
  - `Pillow (PIL)` - Image processing
  - `numpy` - Image array manipulation
  
### Functions
```python
# Extract text from image
def process_image_with_ocr(base64_image: str) -> str:
    image_data = base64.b64decode(base64_image.split(',')[1])
    image = Image.open(io.BytesIO(image_data))
    text = pytesseract.image_to_string(image)
    return text.strip()

# Analyze image properties
def analyze_image_content(base64_image: str) -> dict:
    # Returns: dimensions, format, colors, file size
```

### Frontend
```javascript
// State management
const [uploadedImage, setUploadedImage] = useState(null);
const [generateImage, setGenerateImage] = useState(false);

// Send to API
requestData = {
  message: "Your message",
  image: uploadedImage,  // Base64 string
  generate_image: generateImage
}
```

---

## 🚀 Usage Examples

### Example 1: OCR Screenshot
1. Take screenshot of code/text
2. Click 📷 → select image
3. Type: "Explain this code"
4. AI reads text from image + responds

### Example 2: Meme Analysis
1. Upload meme image
2. Ask: "What's funny about this?"
3. AI reads text + describes humor

### Example 3: Document Processing
1. Upload scanned document
2. Ask: "Translate this to English"
3. AI extracts text + translates

---

## ⚠️ Current Limitations

1. **Image Generation**: Currently only description, not actual image creation
2. **OCR Accuracy**: Depends on image quality and text clarity
3. **Language Support**: Tesseract works best with English/Croatian
4. **File Size**: Large images (>10MB) may be slow

---

## 🔮 Future Enhancements

- [ ] Stable Diffusion integration for real image generation
- [ ] DALL-E API integration
- [ ] Image-to-image transformations
- [ ] Advanced OCR with multiple languages
- [ ] Handwriting recognition
- [ ] Object detection in images

---

## 🧪 Testing

Test the system:
```bash
# 1. Backend must be running
cd /root/MasterCoderAI/backend
/root/MasterCoderAI/.venv/bin/python -m uvicorn api.main:app --host 0.0.0.0 --port 8000

# 2. Frontend must be built
cd /root/MasterCoderAI/frontend
npm run build

# 3. Access: http://YOUR_IP:3000
# 4. Upload test image with text
# 5. Check console for debug logs
```

---

## 📦 Installation Requirements

All dependencies are in:
- **install.sh** - Auto-installs everything
- **requirements.txt** - Python packages

```bash
# System packages
tesseract-ocr

# Python packages
pillow>=10.0.0
pytesseract>=0.3.10
numpy>=1.24.0
```

---

**Status**: ✅ **FULLY FUNCTIONAL** (OCR working, image generation pending real implementation)
