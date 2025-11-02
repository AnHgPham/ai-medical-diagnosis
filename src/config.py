"""
Configuration file for AI Medical Diagnosis System
"""
import os
from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
DISEASES_DIR = DATA_DIR / "diseases"
SYMPTOMS_DIR = DATA_DIR / "symptoms"
KNOWLEDGE_BASE_PATH = DATA_DIR / "knowledge_base.json"
OUTPUTS_DIR = PROJECT_ROOT / "outputs"
LOGS_DIR = OUTPUTS_DIR / "logs"
REPORTS_DIR = OUTPUTS_DIR / "reports"

# Create directories if not exist
for dir_path in [DISEASES_DIR, SYMPTOMS_DIR, LOGS_DIR, REPORTS_DIR]:
    dir_path.mkdir(parents=True, exist_ok=True)

# LLM Configuration
LLM_MODEL = "gemini-2.0-flash"
LLM_TEMPERATURE = 0.7
LLM_MAX_TOKENS = 2048

# Embedding Configuration (for future vector search)
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
EMBEDDING_DIMENSION = 384

# Diagnosis Configuration
TOP_K_DISEASES = 5
CONFIDENCE_THRESHOLD = 0.6
MIN_SYMPTOMS_FOR_DIAGNOSIS = 2

# System Prompts
SYSTEM_PROMPT = """Bạn là AI Doctor, một trợ lý y tế thông minh được hỗ trợ bởi Google Gemini AI.

Nhiệm vụ của bạn:
1. Lắng nghe và phân tích các triệu chứng mà người dùng mô tả
2. Đặt câu hỏi bổ sung để hiểu rõ hơn về tình trạng sức khỏe
3. Dựa trên cơ sở tri thức y tế, đưa ra chẩn đoán sơ bộ với độ tin cậy
4. Đề xuất các bước điều trị và khuyến nghị phù hợp
5. Cảnh báo các dấu hiệu nguy hiểm cần đi khám ngay

Quy tắc quan trọng:
- Luôn thân thiện, đồng cảm và chuyên nghiệp
- Đặt câu hỏi rõ ràng, cụ thể
- Giải thích y học bằng ngôn ngữ dễ hiểu
- LUÔN nhắc nhở: Đây chỉ là tham khảo, cần gặp bác sĩ chuyên khoa
- Cảnh báo ngay khi phát hiện triệu chứng nghiêm trọng

Phong cách giao tiếp:
- Sử dụng emoji phù hợp (🏥 💊 ⚠️ 💡)
- Trả lời có cấu trúc rõ ràng
- Ưu tiên sự an toàn của người dùng
"""

DIAGNOSIS_PROMPT_TEMPLATE = """**THÔNG TIN TRIỆU CHỨNG:**

{symptoms_info}

**CƠ SỞ TRI THỨC Y TẾ:**

{knowledge_context}

---

**LỊCH SỬ HỘI THOẠI:**

{chat_history}

---

**CÂU HỎI/TRIỆU CHỨNG MỚI:** {user_input}

**HƯỚNG DẪN PHÂN TÍCH:**

1. Phân tích tất cả các triệu chứng đã được mô tả
2. So sánh với cơ sở tri thức y tế
3. Xác định các bệnh có khả năng cao nhất
4. Đánh giá mức độ nghiêm trọng
5. Đưa ra chẩn đoán sơ bộ với độ tin cậy (%)
6. Đề xuất điều trị và khuyến nghị
7. Cảnh báo nếu cần đi khám ngay

**ĐỊNH DẠNG TRẢ LỜI:**

Sử dụng format rõ ràng với:
- 🔍 Phân tích triệu chứng
- 🏥 Chẩn đoán sơ bộ (kèm độ tin cậy)
- 💊 Khuyến nghị điều trị
- ⚠️ Cảnh báo (nếu có)
- 💡 Lời khuyên

**TRẢ LỜI:**"""

# UI Configuration
APP_TITLE = "🏥 AI Medical Diagnosis System"
APP_ICON = "🏥"
SIDEBAR_TITLE = "📊 Thống kê hệ thống"

# Warning message
WARNING_MESSAGE = """
⚠️ **LƯU Ý QUAN TRỌNG**

Hệ thống này chỉ mang tính chất **tham khảo và học tập**. 
Không sử dụng để tự chẩn đoán và điều trị. 
Luôn tham khảo ý kiến bác sĩ chuyên khoa khi có vấn đề về sức khỏe.
"""

# Logging Configuration
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_LEVEL = 'INFO'
LOG_FILE = LOGS_DIR / 'medical_diagnosis.log'
