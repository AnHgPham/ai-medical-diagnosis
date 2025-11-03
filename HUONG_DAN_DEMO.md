# Hướng Dẫn Demo Hệ Thống AI Medical Diagnosis

**Tài liệu này hướng dẫn cách demo và trình bày hệ thống chẩn đoán y tế thông minh.**

---

## 📋 Mục Lục

1. Chuẩn Bị Demo
2. Kịch Bản Demo
3. Các Tính Năng Cần Trình Bày
4. Câu Hỏi Thường Gặp

---

## 1. Chuẩn Bị Demo

### 1.1. Kiểm Tra Hệ Thống

Trước khi demo, hãy đảm bảo:

✅ **Ứng dụng đang chạy:**
- Truy cập: [https://ai-medical.streamlit.app/](https://ai-medical.streamlit.app/)
- Kiểm tra app có load được không
- Thử gửi một tin nhắn test

✅ **Chuẩn bị các kịch bản:**
- Kịch bản 1: Triệu chứng thông thường (cảm cúm)
- Kịch bản 2: Triệu chứng khẩn cấp (đau ngực)
- Kịch bản 3: Hội thoại nhiều lượt

✅ **Tài liệu hỗ trợ:**
- Báo cáo kỹ thuật
- Slide trình bày (nếu có)
- Code trên GitHub

### 1.2. Thiết Bị

- **Máy tính:** Có kết nối internet ổn định
- **Trình duyệt:** Chrome, Firefox, hoặc Edge (phiên bản mới nhất)
- **Màn hình:** Độ phân giải tối thiểu 1280x720
- **Backup:** Có video demo sẵn phòng trường hợp mất kết nối

---

## 2. Kịch Bản Demo

### Kịch Bản 1: Triệu Chứng Thông Thường (Cảm Cúm)

**Mục tiêu:** Cho thấy khả năng chẩn đoán sơ bộ của hệ thống.

**Bước 1:** Mở ứng dụng
- Truy cập [https://ai-medical.streamlit.app/](https://ai-medical.streamlit.app/)
- Giới thiệu giao diện:
  - Header với tên hệ thống
  - Warning box (lưu ý quan trọng)
  - Sidebar với thông tin về AI
  - Khu vực chat chính

**Bước 2:** Nhập triệu chứng đơn giản
```
Người dùng: Tôi bị sốt và ho
```

**Bước 3:** Quan sát phản hồi của AI
- AI sẽ hỏi thêm thông tin:
  - Sốt cao bao nhiêu độ?
  - Ho có đờm không?
  - Kéo dài bao lâu?

**Bước 4:** Cung cấp thông tin chi tiết
```
Người dùng: Tôi sốt 38.5 độ, ho có đờm, đã 2 ngày rồi
```

**Bước 5:** Nhận chẩn đoán
- AI sẽ đưa ra:
  - Chẩn đoán sơ bộ (ví dụ: Cảm cúm, viêm đường hô hấp)
  - Độ tin cậy (%)
  - Giải thích lý do
  - Khuyến nghị điều trị
  - Lưu ý khi nào cần gặp bác sĩ

**Điểm nhấn:**
- ✅ AI hiểu ngôn ngữ tự nhiên
- ✅ Đặt câu hỏi bổ sung thông minh
- ✅ Chẩn đoán logic và có giải thích
- ✅ Khuyến nghị an toàn

---

### Kịch Bản 2: Triệu Chứng Khẩn Cấp (Đau Ngực)

**Mục tiêu:** Cho thấy khả năng phát hiện và cảnh báo khẩn cấp.

**Bước 1:** Nhập triệu chứng nguy hiểm
```
Người dùng: Tôi bị đau ngực dữ dội và khó thở
```

**Bước 2:** Quan sát cảnh báo khẩn cấp
- Hệ thống sẽ **NGAY LẬP TỨC** hiển thị:
  ```
  ⚠️ CẢNH BÁO KHẨN CẤP!
  Triệu chứng 'đau ngực' của bạn có thể rất nghiêm trọng.
  Vui lòng liên hệ cấp cứu (115) hoặc đến cơ sở y tế gần nhất NGAY LẬP TỨC.
  ```

**Bước 3:** Giải thích cơ chế
- Hệ thống có danh sách từ khóa khẩn cấp
- Quét input trước khi gửi tới AI
- Cảnh báo nhanh hơn, không phụ thuộc vào AI

**Điểm nhấn:**
- ✅ Phát hiện khẩn cấp nhanh chóng
- ✅ Cảnh báo rõ ràng, nổi bật
- ✅ Hướng dẫn hành động cụ thể
- ✅ Ưu tiên an toàn người dùng

---

### Kịch Bản 3: Hội Thoại Nhiều Lượt

**Mục tiêu:** Cho thấy khả năng duy trì ngữ cảnh trong cuộc trò chuyện.

**Lượt 1:**
```
Người dùng: Tôi bị đau đầu
```

**Lượt 2:**
```
AI: Bạn có thể mô tả thêm về cơn đau đầu không?
Người dùng: Đau ở vùng thái dương, nhức nhối
```

**Lượt 3:**
```
AI: Bạn có căng thẳng hoặc mệt mỏi gần đây không?
Người dùng: Có, tôi làm việc nhiều và ngủ ít
```

**Lượt 4:**
```
AI: Dựa trên các triệu chứng, có thể bạn bị đau đầu căng thẳng...
```

**Điểm nhấn:**
- ✅ AI nhớ lịch sử hội thoại
- ✅ Đặt câu hỏi có liên quan đến câu trả lời trước
- ✅ Chẩn đoán dựa trên toàn bộ thông tin

---

## 3. Các Tính Năng Cần Trình Bày

### 3.1. Chức Năng Chính

| Tính Năng | Mô Tả | Demo |
|-----------|-------|------|
| **Phân tích triệu chứng** | AI hiểu và phân tích triệu chứng bằng ngôn ngữ tự nhiên | Kịch bản 1 |
| **Chẩn đoán sơ bộ** | Đưa ra danh sách bệnh có khả năng cao với độ tin cậy | Kịch bản 1 |
| **Cảnh báo khẩn cấp** | Phát hiện và cảnh báo triệu chứng nguy hiểm | Kịch bản 2 |
| **Tư vấn điều trị** | Hướng dẫn chăm sóc tại nhà và khi nào cần gặp bác sĩ | Kịch bản 1 |
| **Quản lý hội thoại** | Duy trì ngữ cảnh qua nhiều lượt chat | Kịch bản 3 |

### 3.2. Điểm Nổi Bật Kỹ Thuật

**1. Kiến Trúc Modular**
- Code được tổ chức thành các module độc lập
- Dễ bảo trì và mở rộng
- Hiển thị cấu trúc thư mục trên GitHub

**2. Testing Toàn Diện**
- 80+ test cases
- Coverage > 85%
- Chạy demo test: `pytest tests/ -v`

**3. AI-Direct Approach**
- Sử dụng Google Gemini 2.0 Flash
- Không cần xây dựng knowledge base thủ công
- Tri thức sâu rộng, cập nhật liên tục

**4. Prompt Engineering**
- System prompt được thiết kế cẩn thận
- Định hướng AI đóng vai bác sĩ chuyên nghiệp
- Đảm bảo an toàn và đạo đức

**5. UI/UX Hiện Đại**
- Giao diện sạch sẽ, trực quan
- Responsive design
- Màu sắc và typography chuyên nghiệp

---

## 4. Câu Hỏi Thường Gặp

### Q1: Hệ thống có thể chẩn đoán bao nhiêu loại bệnh?

**Trả lời:** Hệ thống sử dụng Google Gemini AI, có kiến thức về hàng ngàn bệnh lý phổ biến và hiếm gặp. Không giới hạn số lượng bệnh như các hệ thống rule-based truyền thống.

### Q2: Độ chính xác của chẩn đoán là bao nhiêu?

**Trả lời:** Hệ thống chỉ đưa ra chẩn đoán **sơ bộ** và **tham khảo**, không thay thế bác sĩ. Độ chính xác phụ thuộc vào:
- Chất lượng thông tin người dùng cung cấp
- Độ phức tạp của triệu chứng
- Khả năng của mô hình Gemini

Qua kiểm thử, AI đưa ra chẩn đoán logic và phù hợp trong hầu hết các trường hợp thông thường.

### Q3: Hệ thống có lưu trữ thông tin cá nhân không?

**Trả lời:** **KHÔNG**. Hệ thống không lưu trữ bất kỳ thông tin cá nhân nào. Lịch sử chat chỉ tồn tại trong phiên làm việc hiện tại và sẽ bị xóa khi đóng trình duyệt.

### Q4: Chi phí vận hành hệ thống?

**Trả lời:** 
- **Hosting:** Miễn phí (Streamlit Community Cloud)
- **AI API:** Miễn phí (Google Gemini free tier)
- **Tổng chi phí:** **$0/tháng**

### Q5: Có thể mở rộng hệ thống không?

**Trả lời:** **CÓ**. Kiến trúc modular cho phép dễ dàng:
- Thêm tính năng mới
- Thay đổi AI model
- Tích hợp với các hệ thống khác
- Hỗ trợ nhiều ngôn ngữ

### Q6: So sánh với các phương pháp truyền thống?

**Trả lời:**

| Tiêu chí | Rule-Based / Ontology | **AI-Direct (Dự án này)** |
|----------|----------------------|---------------------------|
| Tri thức | Giới hạn | **Rất rộng** |
| Linh hoạt | Thấp | **Cao** |
| Bảo trì | Khó | **Dễ** |
| Chi phí xây dựng | Cao | **Thấp** |

### Q7: Hệ thống có được kiểm thử không?

**Trả lời:** **CÓ**. Dự án có bộ test toàn diện:
- 80+ test cases
- 4 loại tests (unit, integration, data quality, input validation)
- Coverage > 85%
- Chạy tự động với Pytest

### Q8: Làm thế nào để chạy hệ thống local?

**Trả lời:**

```bash
# 1. Clone repository
git clone https://github.com/AnHgPham/ai-medical-diagnosis.git
cd ai-medical-diagnosis

# 2. Cài đặt dependencies
pip install -r requirements.txt

# 3. Tạo file .streamlit/secrets.toml và thêm API key
GEMINI_API_KEY = "your-api-key-here"

# 4. Chạy app
streamlit run app.py
```

---

## 5. Tips Để Demo Thành Công

### ✅ Trước Demo

1. **Test kỹ:** Chạy thử tất cả kịch bản trước
2. **Backup:** Có video demo phòng khi mất kết nối
3. **Tài liệu:** In báo cáo và slide ra giấy
4. **Thời gian:** Luyện tập để demo trong 10-15 phút

### ✅ Trong Demo

1. **Tự tin:** Nói chậm, rõ ràng
2. **Tương tác:** Hỏi khán giả có câu hỏi không
3. **Linh hoạt:** Sẵn sàng điều chỉnh kịch bản
4. **Nhấn mạnh:** Các điểm mạnh của hệ thống

### ✅ Sau Demo

1. **Q&A:** Trả lời câu hỏi một cách tự tin
2. **Tài liệu:** Chia sẻ link GitHub và live demo
3. **Feedback:** Ghi nhận ý kiến để cải thiện

---

## 6. Checklist Demo

- [ ] Kiểm tra app đang chạy
- [ ] Chuẩn bị 3 kịch bản demo
- [ ] Test kết nối internet
- [ ] Mở sẵn các tab cần thiết
- [ ] Chuẩn bị backup (video/screenshots)
- [ ] In tài liệu hỗ trợ
- [ ] Luyện tập demo 2-3 lần
- [ ] Chuẩn bị trả lời câu hỏi

---

**Chúc bạn demo thành công! 🎉**

**Live Demo:** [https://ai-medical.streamlit.app/](https://ai-medical.streamlit.app/)  
**GitHub:** [https://github.com/AnHgPham/ai-medical-diagnosis](https://github.com/AnHgPham/ai-medical-diagnosis)
