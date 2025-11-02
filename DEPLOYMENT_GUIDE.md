# 🚀 Hướng dẫn Deploy lên Streamlit Cloud

## Bước 1: Chuẩn bị Gemini API Key

### 1.1. Lấy API Key miễn phí

1. Truy cập: https://makersuite.google.com/app/apikey
2. Đăng nhập bằng Google Account
3. Click **"Create API Key"**
4. Copy API key (dạng: `AIzaSy...`)

**💡 Lưu ý:** Gemini API có free tier rất hào phóng:
- 60 requests/phút
- Miễn phí hoàn toàn
- Không cần thẻ tín dụng

---

## Bước 2: Push Code lên GitHub

### 2.1. Tạo Repository mới

1. Truy cập https://github.com
2. Click **"New repository"**
3. Đặt tên: `ai-medical-diagnosis`
4. Chọn **Public**
5. Click **"Create repository"**

### 2.2. Upload Code

**Cách 1: Qua Web Interface (Dễ nhất)**

1. Vào repository vừa tạo
2. Click **"uploading an existing file"**
3. Kéo thả các file:
   - `app.py`
   - `knowledge_base.json`
   - `requirements.txt`
   - `.streamlit/config.toml`
4. Click **"Commit changes"**

**Cách 2: Qua Git Command Line**

```bash
cd diagnosis_streamlit

# Khởi tạo git
git init

# Thêm remote
git remote add origin https://github.com/YOUR_USERNAME/ai-medical-diagnosis.git

# Add files
git add .

# Commit
git commit -m "Initial commit"

# Push
git push -u origin main
```

**⚠️ Quan trọng:** Không commit file `.streamlit/secrets.toml` (nếu có)

---

## Bước 3: Deploy lên Streamlit Cloud

### 3.1. Tạo tài khoản Streamlit Cloud

1. Truy cập: https://streamlit.io/cloud
2. Click **"Sign up"**
3. Chọn **"Continue with GitHub"**
4. Authorize Streamlit

### 3.2. Deploy App

1. Click **"New app"**
2. Chọn:
   - **Repository:** `YOUR_USERNAME/ai-medical-diagnosis`
   - **Branch:** `main`
   - **Main file path:** `app.py`
3. Click **"Advanced settings"**
4. Trong **Secrets**, thêm:

```toml
GEMINI_API_KEY = "AIzaSy...YOUR_API_KEY..."
```

5. Click **"Deploy!"**

### 3.3. Đợi Deploy

- Quá trình deploy mất khoảng 2-5 phút
- Bạn sẽ thấy logs đang chạy
- Khi xong, app sẽ tự động mở

---

## Bước 4: Kiểm tra và Sử dụng

### 4.1. URL của bạn

App sẽ có URL dạng:
```
https://YOUR_USERNAME-ai-medical-diagnosis-app-xxxxx.streamlit.app
```

### 4.2. Test App

1. Mở URL
2. Nhập triệu chứng vào chat
3. Kiểm tra AI có phản hồi không

**Ví dụ test:**
```
"Tôi bị sốt cao 39 độ, ho nhiều và đau cơ"
```

---

## Bước 5: Quản lý và Cập nhật

### 5.1. Cập nhật Code

Mỗi khi bạn push code mới lên GitHub, Streamlit sẽ tự động deploy lại:

```bash
# Sửa code
git add .
git commit -m "Update features"
git push
```

### 5.2. Xem Logs

1. Vào https://share.streamlit.io
2. Click vào app của bạn
3. Click **"Manage app"** → **"Logs"**

### 5.3. Restart App

Nếu app bị lỗi:
1. Vào **"Manage app"**
2. Click **"Reboot app"**

---

## 📋 Checklist Deploy

- [ ] Đã có Gemini API Key
- [ ] Đã tạo GitHub repository
- [ ] Đã upload code lên GitHub
- [ ] Đã tạo tài khoản Streamlit Cloud
- [ ] Đã thêm API key vào Secrets
- [ ] Đã deploy thành công
- [ ] Đã test app hoạt động

---

## ⚠️ Xử lý Lỗi Thường gặp

### Lỗi 1: "GEMINI_API_KEY not found"

**Nguyên nhân:** Chưa thêm API key vào Secrets

**Giải pháp:**
1. Vào **Manage app** → **Settings** → **Secrets**
2. Thêm: `GEMINI_API_KEY = "your-key"`
3. Click **Save**

### Lỗi 2: "Module not found"

**Nguyên nhân:** Thiếu thư viện trong `requirements.txt`

**Giải pháp:**
1. Kiểm tra file `requirements.txt`
2. Đảm bảo có:
```
streamlit==1.29.0
google-generativeai==0.3.2
```

### Lỗi 3: "Rate limit exceeded"

**Nguyên nhân:** Vượt quá giới hạn API (60 requests/phút)

**Giải pháp:**
- Đợi 1 phút rồi thử lại
- Hoặc nâng cấp Gemini API plan

### Lỗi 4: App bị "sleep"

**Nguyên nhân:** Streamlit Cloud free tier sẽ sleep app sau 7 ngày không dùng

**Giải pháp:**
- Truy cập app để "đánh thức"
- Hoặc nâng cấp lên paid plan

---

## 💰 Chi phí

### Streamlit Cloud
- **Free tier:** 
  - 1 private app
  - Unlimited public apps
  - 1 GB RAM
  - Shared CPU
  - **Miễn phí vĩnh viễn**

### Gemini API
- **Free tier:**
  - 60 requests/phút
  - Unlimited requests/ngày
  - **Miễn phí vĩnh viễn**

**Tổng chi phí: $0/tháng** ✨

---

## 🎯 Các Bước Tiếp theo

### Tùy chỉnh Domain

1. Vào **Manage app** → **Settings**
2. Thay đổi **App URL**
3. Ví dụ: `ai-doctor-vietnam.streamlit.app`

### Thêm Tính năng

- [ ] Lưu lịch sử chat
- [ ] Export kết quả PDF
- [ ] Đa ngôn ngữ
- [ ] Phân tích hình ảnh

### Chia sẻ

- Chia sẻ URL với bạn bè
- Đăng lên social media
- Thêm vào portfolio

---

## 📞 Hỗ trợ

**Gặp vấn đề?**
- Streamlit Docs: https://docs.streamlit.io
- Gemini API Docs: https://ai.google.dev/docs
- Community: https://discuss.streamlit.io

---

**🎉 Chúc mừng! App của bạn đã online vĩnh viễn và hoàn toàn miễn phí!**
