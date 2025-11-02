# 🤖 AI Medical Diagnosis System

**Streamlit + Google Gemini AI**

Hệ thống chẩn đoán y tế thông minh sử dụng Google Gemini AI với giao diện chat đơn giản và hiện đại.

---

## ✨ Tính năng

- 💬 **Chat với AI Doctor** - Trò chuyện tự nhiên như với bác sĩ thật
- 🧠 **Phân tích thông minh** - Sử dụng Google Gemini Pro
- 📊 **Chẩn đoán chi tiết** - Kèm độ tin cậy và giải thích
- 💊 **Khuyến nghị điều trị** - Hướng dẫn cụ thể
- ⚠️ **Cảnh báo nguy hiểm** - Nhận diện triệu chứng nghiêm trọng

---

## 🚀 Demo

**Live Demo:** [Đang deploy...]

---

## 🛠️ Công nghệ

| Thành phần | Công nghệ |
|------------|-----------|
| **Framework** | Streamlit |
| **AI Model** | Google Gemini Pro |
| **Language** | Python 3.11 |
| **Deployment** | Streamlit Cloud |
| **Cost** | **$0/tháng** (Hoàn toàn miễn phí) |

---

## 📦 Cài đặt Local

### Yêu cầu

- Python 3.11+
- Gemini API Key (miễn phí)

### Các bước

1. **Clone repository:**
```bash
git clone https://github.com/YOUR_USERNAME/ai-medical-diagnosis.git
cd ai-medical-diagnosis
```

2. **Cài đặt dependencies:**
```bash
pip install -r requirements.txt
```

3. **Tạo file secrets:**
```bash
mkdir .streamlit
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
```

4. **Thêm API key vào `.streamlit/secrets.toml`:**
```toml
GEMINI_API_KEY = "your-api-key-here"
```

Lấy API key tại: https://makersuite.google.com/app/apikey

5. **Chạy app:**
```bash
streamlit run app.py
```

6. **Mở trình duyệt:**
```
http://localhost:8501
```

---

## 🌐 Deploy lên Streamlit Cloud

Xem hướng dẫn chi tiết trong file [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)

**Tóm tắt:**
1. Lấy Gemini API Key (miễn phí)
2. Push code lên GitHub
3. Deploy trên Streamlit Cloud
4. Thêm API key vào Secrets
5. Done! App online vĩnh viễn

**Chi phí: $0** ✨

---

## 📁 Cấu trúc Dự án

```
diagnosis_streamlit/
├── app.py                          # Streamlit app chính
├── knowledge_base.json             # Cơ sở tri thức y tế
├── requirements.txt                # Python dependencies
├── .streamlit/
│   ├── config.toml                # Streamlit configuration
│   └── secrets.toml.example       # Template cho API key
├── DEPLOYMENT_GUIDE.md            # Hướng dẫn deploy chi tiết
└── README.md                       # File này
```

---

## 💬 Cách Sử dụng

### Ví dụ 1: Mô tả triệu chứng đơn giản

**Bạn:**
```
Tôi bị sốt và ho
```

**AI Doctor:**
```
Bạn có thể cho tôi biết thêm:
- Sốt của bạn cao không? Bao nhiêu độ?
- Ho có đờm không?
- Triệu chứng kéo dài bao lâu rồi?
```

### Ví dụ 2: Mô tả chi tiết

**Bạn:**
```
Tôi bị sốt cao 39 độ, ho nhiều, đau cơ và rất mệt mỏi. 
Triệu chứng đã kéo dài 3 ngày.
```

**AI Doctor:**
```
Dựa trên các triệu chứng bạn mô tả, tôi phân tích như sau:

🔍 Chẩn đoán có khả năng cao nhất:

1. Cúm (Influenza) - Độ tin cậy: 85%
   - Lý do: Sốt cao (39°C), ho, đau cơ và mệt mỏi là các 
     triệu chứng điển hình của cúm...
   
2. COVID-19 - Độ tin cậy: 60%
   - Lý do: Các triệu chứng tương tự cúm...

💊 Khuyến nghị:
- Nghỉ ngơi đầy đủ
- Uống nhiều nước
- Dùng thuốc hạ sốt nếu cần
- Nên làm xét nghiệm để xác định chính xác

⚠️ Cảnh báo:
Nếu xuất hiện khó thở, đau ngực, hoặc sốt kéo dài 
trên 5 ngày, hãy đến cơ sở y tế ngay lập tức.
```

---

## 🎯 Cơ sở Tri thức

Hệ thống hiện tại hỗ trợ chẩn đoán:

| Bệnh | Triệu chứng chính | Mức độ |
|------|-------------------|---------|
| **Cúm (Influenza)** | Sốt cao, ho, đau cơ, mệt mỏi | Trung bình |
| **Cảm lạnh** | Sổ mũi, hắt hơi, đau họng | Nhẹ |
| **COVID-19** | Sốt, ho, mất vị giác | Nghiêm trọng |
| **Viêm mũi dị ứng** | Ngứa mắt, hắt hơi, sổ mũi | Nhẹ |
| **Viêm phế quản** | Ho có đờm, khó thở | Trung bình |

**Tổng cộng:** 5 bệnh, 16 triệu chứng

---

## ⚠️ Lưu ý Quan trọng

1. **Không thay thế bác sĩ:** Hệ thống chỉ hỗ trợ, không thay thế chẩn đoán y khoa chuyên nghiệp.

2. **Chỉ tham khảo:** Luôn tham khảo ý kiến bác sĩ khi có vấn đề sức khỏe.

3. **Giới hạn:** Chỉ biết về 5 bệnh phổ biến trong cơ sở tri thức.

4. **Ngôn ngữ:** Chủ yếu tiếng Việt.

---

## 📊 So sánh với Phiên bản Cũ

| Tính năng | Flask + OpenAI | **Streamlit + Gemini** |
|-----------|----------------|------------------------|
| **Giao diện** | 3 tabs (Checkbox + Text + Chat) | **Chỉ Chat (Đơn giản hơn)** |
| **AI Model** | OpenAI GPT-4 | **Google Gemini Pro** |
| **Chi phí API** | ~$0.005/lần | **Miễn phí** |
| **Deploy** | Cần server | **Streamlit Cloud (Free)** |
| **Độ phức tạp** | Cao | **Thấp (Dễ maintain)** |
| **Tốc độ** | 3-5s | **2-4s** |

---

## 🚀 Hướng Phát triển

- [ ] Mở rộng cơ sở tri thức (20-50 bệnh)
- [ ] Lưu lịch sử chat
- [ ] Export kết quả PDF
- [ ] Đa ngôn ngữ (English, Chinese)
- [ ] Phân tích hình ảnh (X-ray, CT)
- [ ] Tích hợp với wearable devices
- [ ] Fine-tune Gemini cho y tế Việt Nam

---

## 🤝 Đóng góp

Mọi đóng góp đều được hoan nghênh!

1. Fork repository
2. Tạo branch mới (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Mở Pull Request

---

## 📄 License

Dự án này được phát triển cho mục đích học thuật và nghiên cứu.

---

## 👨‍💻 Tác giả

**Manus AI**  
Ngày: 02 tháng 11 năm 2025

---

## 📞 Liên hệ

- **Email:** contact@ai-diagnosis-system.com
- **GitHub:** [Your GitHub Profile]
- **Demo:** [Your Streamlit App URL]

---

## 🙏 Cảm ơn

- **Google Gemini** - Cung cấp AI model miễn phí
- **Streamlit** - Framework tuyệt vời và hosting miễn phí
- **Cộng đồng Python** - Các thư viện mã nguồn mở

---

**⚕️ Luôn tham khảo ý kiến bác sĩ chuyên khoa khi có vấn đề về sức khỏe!**
