# ⚡ Quick Start Guide

## 🎯 Deploy trong 5 phút!

### Bước 1: Lấy Gemini API Key (1 phút)

1. Vào: https://makersuite.google.com/app/apikey
2. Click **"Create API Key"**
3. Copy key (dạng: `AIzaSy...`)

✅ **Miễn phí vĩnh viễn!**

---

### Bước 2: Upload lên GitHub (2 phút)

1. Vào: https://github.com/new
2. Tạo repo tên: `ai-medical-diagnosis`
3. Chọn **Public**
4. Click **"uploading an existing file"**
5. Kéo thả tất cả file trong thư mục này
6. Click **"Commit"**

---

### Bước 3: Deploy lên Streamlit (2 phút)

1. Vào: https://streamlit.io/cloud
2. Click **"Sign up with GitHub"**
3. Click **"New app"**
4. Chọn repo: `ai-medical-diagnosis`
5. Main file: `app.py`
6. Click **"Advanced settings"**
7. Thêm vào Secrets:
```toml
GEMINI_API_KEY = "AIzaSy...YOUR_KEY..."
```
8. Click **"Deploy!"**

---

### ✅ Done!

App của bạn sẽ online tại:
```
https://YOUR_USERNAME-ai-medical-diagnosis-xxxxx.streamlit.app
```

**Chi phí: $0/tháng** 🎉

---

## 🧪 Test Local (Tùy chọn)

```bash
# Cài đặt
pip install -r requirements.txt

# Tạo secrets
mkdir -p .streamlit
echo 'GEMINI_API_KEY = "your-key"' > .streamlit/secrets.toml

# Chạy
streamlit run app.py
```

---

## ❓ Gặp vấn đề?

Xem hướng dẫn chi tiết trong [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)

---

**🚀 Chúc mừng! App của bạn đã online!**
