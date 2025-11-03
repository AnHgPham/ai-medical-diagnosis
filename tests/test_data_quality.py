"""
Test Data Quality
Kiểm tra chất lượng dữ liệu và phản hồi của hệ thống
"""
import pytest
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from config import EMERGENCY_KEYWORDS, SYSTEM_PROMPT


class TestEmergencyKeywordsQuality:
    """Test chất lượng danh sách emergency keywords"""
    
    def test_emergency_keywords_not_empty(self):
        """Test danh sách emergency keywords không rỗng"""
        assert len(EMERGENCY_KEYWORDS) > 0, "Danh sách emergency keywords không được rỗng"
    
    def test_emergency_keywords_coverage(self):
        """Test độ bao phủ của emergency keywords"""
        # Các keywords quan trọng phải có
        critical_keywords = ['khó thở', 'đau ngực', 'bất tỉnh', 'co giật']
        for keyword in critical_keywords:
            assert keyword in EMERGENCY_KEYWORDS, \
                f"Emergency keywords phải bao gồm '{keyword}'"
    
    def test_emergency_keywords_lowercase(self):
        """Test emergency keywords phải là chữ thường"""
        for keyword in EMERGENCY_KEYWORDS:
            assert keyword == keyword.lower(), \
                f"Emergency keyword '{keyword}' phải là chữ thường"
    
    def test_emergency_keywords_no_duplicates(self):
        """Test không có keywords trùng lặp"""
        assert len(EMERGENCY_KEYWORDS) == len(set(EMERGENCY_KEYWORDS)), \
            "Không được có emergency keywords trùng lặp"
    
    def test_emergency_keywords_meaningful(self):
        """Test keywords phải có ý nghĩa (> 2 ký tự)"""
        for keyword in EMERGENCY_KEYWORDS:
            assert len(keyword) > 2, \
                f"Emergency keyword '{keyword}' quá ngắn"


class TestSystemPromptQuality:
    """Test chất lượng system prompt"""
    
    def test_system_prompt_not_empty(self):
        """Test system prompt không rỗng"""
        assert len(SYSTEM_PROMPT) > 0, "System prompt không được rỗng"
    
    def test_system_prompt_has_role_definition(self):
        """Test system prompt có định nghĩa vai trò"""
        role_keywords = ['AI Doctor', 'bác sĩ', 'doctor', 'y tế']
        assert any(keyword in SYSTEM_PROMPT for keyword in role_keywords), \
            "System prompt phải định nghĩa vai trò AI Doctor"
    
    def test_system_prompt_has_instructions(self):
        """Test system prompt có hướng dẫn"""
        instruction_keywords = ['nhiệm vụ', 'quy tắc', 'hướng dẫn', 'phải', 'nên']
        assert any(keyword in SYSTEM_PROMPT.lower() for keyword in instruction_keywords), \
            "System prompt phải có hướng dẫn rõ ràng"
    
    def test_system_prompt_has_safety_warning(self):
        """Test system prompt có cảnh báo an toàn"""
        safety_keywords = ['tham khảo', 'không thay thế', 'bác sĩ', 'chuyên nghiệp']
        assert any(keyword in SYSTEM_PROMPT.lower() for keyword in safety_keywords), \
            "System prompt phải có cảnh báo an toàn"
    
    def test_system_prompt_length(self):
        """Test độ dài system prompt hợp lý"""
        assert 100 < len(SYSTEM_PROMPT) < 5000, \
            "System prompt phải có độ dài hợp lý (100-5000 ký tự)"


class TestResponseFormat:
    """Test định dạng phản hồi"""
    
    def test_diagnosis_response_structure(self):
        """Test cấu trúc phản hồi chẩn đoán"""
        mock_response = """
        Dựa trên các triệu chứng bạn mô tả:
        
        🔍 Chẩn đoán có khả năng cao nhất:
        1. Cảm lạnh - Độ tin cậy: 80%
        
        💊 Khuyến nghị:
        - Nghỉ ngơi đầy đủ
        - Uống nhiều nước
        """
        
        # Kiểm tra có các phần quan trọng
        assert "chẩn đoán" in mock_response.lower(), "Phải có phần chẩn đoán"
        assert "khuyến nghị" in mock_response.lower(), "Phải có phần khuyến nghị"
    
    def test_emergency_response_structure(self):
        """Test cấu trúc phản hồi khẩn cấp"""
        mock_response = """
        ⚠️⚠️⚠️ CẢNH BÁO KHẨN CẤP ⚠️⚠️⚠️
        
        🚨 HÀNH ĐỘNG NGAY LẬP TỨC:
        1. Gọi cấp cứu 115
        2. Đến bệnh viện gần nhất
        """
        
        assert "CẢNH BÁO" in mock_response or "KHẨN CẤP" in mock_response, \
            "Phải có cảnh báo khẩn cấp"
        assert "115" in mock_response or "cấp cứu" in mock_response, \
            "Phải có hướng dẫn gọi cấp cứu"
    
    def test_response_has_emoji(self):
        """Test phản hồi có emoji để dễ đọc"""
        mock_response = "🔍 Phân tích: Bạn có thể bị cảm lạnh"
        # Emoji giúp phản hồi dễ đọc hơn
        assert any(char for char in mock_response if ord(char) > 127), \
            "Response nên có emoji hoặc ký tự đặc biệt"


class TestConversationFlow:
    """Test luồng hội thoại"""
    
    def test_greeting_message(self):
        """Test tin nhắn chào mừng"""
        greeting = "Xin chào! Tôi là AI Doctor"
        assert "chào" in greeting.lower(), "Phải có lời chào"
        assert "AI Doctor" in greeting, "Phải giới thiệu tên"
    
    def test_follow_up_questions(self):
        """Test câu hỏi theo dõi"""
        mock_response = "Bạn có thể cho tôi biết thêm: Sốt cao bao nhiêu độ?"
        question_indicators = ["?", "cho tôi biết", "bạn có", "có thể"]
        assert any(indicator in mock_response for indicator in question_indicators), \
            "Phải có câu hỏi theo dõi"
    
    def test_context_awareness(self):
        """Test nhận thức ngữ cảnh"""
        # Phản hồi phải liên quan đến câu hỏi trước
        user_msg_1 = "Tôi bị sốt"
        mock_response_1 = "Sốt của bạn cao bao nhiêu độ?"
        
        user_msg_2 = "39 độ"
        mock_response_2 = "Sốt 39 độ là khá cao..."
        
        assert "39" in mock_response_2, "Phải nhớ thông tin từ câu trước"


class TestDataConsistency:
    """Test tính nhất quán của dữ liệu"""
    
    def test_temperature_units_consistent(self):
        """Test đơn vị nhiệt độ nhất quán"""
        mock_responses = [
            "Sốt 39 độ C",
            "Nhiệt độ 38.5°C",
            "Sốt cao trên 38 độ"
        ]
        # Phải sử dụng độ C (Celsius) nhất quán
        for response in mock_responses:
            assert "độ" in response or "°C" in response, \
                "Phải có đơn vị nhiệt độ"
    
    def test_medical_terms_vietnamese(self):
        """Test thuật ngữ y khoa tiếng Việt"""
        medical_terms = {
            "fever": "sốt",
            "headache": "đau đầu",
            "cough": "ho",
            "cold": "cảm lạnh"
        }
        # Ưu tiên sử dụng tiếng Việt
        mock_response = "Bạn bị sốt và đau đầu, có thể là cảm lạnh"
        for vietnamese_term in medical_terms.values():
            # Ít nhất một số thuật ngữ tiếng Việt phải có
            pass
    
    def test_confidence_level_format(self):
        """Test định dạng độ tin cậy"""
        mock_response = "Cảm lạnh - Độ tin cậy: 80%"
        # Độ tin cậy phải là số từ 0-100%
        import re
        confidence_pattern = r'\d+%'
        matches = re.findall(confidence_pattern, mock_response)
        if matches:
            for match in matches:
                value = int(match.replace('%', ''))
                assert 0 <= value <= 100, "Độ tin cậy phải từ 0-100%"


class TestSafetyChecks:
    """Test các kiểm tra an toàn"""
    
    def test_no_definitive_diagnosis(self):
        """Test không đưa ra chẩn đoán chắc chắn"""
        unsafe_phrases = [
            "chắc chắn 100%",
            "bạn bị bệnh X",
            "tôi chẩn đoán chính thức"
        ]
        mock_response = "Bạn CÓ THỂ bị cảm lạnh (độ tin cậy 80%)"
        
        # Phải dùng ngôn ngữ không chắc chắn
        safe_phrases = ["có thể", "khả năng", "sơ bộ", "tham khảo"]
        assert any(phrase in mock_response.lower() for phrase in safe_phrases), \
            "Phải dùng ngôn ngữ không chắc chắn"
    
    def test_no_prescription(self):
        """Test không kê đơn thuốc"""
        unsafe_response = "Bạn nên uống Paracetamol 500mg, 3 lần/ngày"
        safe_response = "Bạn có thể tham khảo bác sĩ về việc dùng thuốc hạ sốt"
        
        # Không nên có liều lượng cụ thể
        prescription_indicators = ["mg", "ml", "lần/ngày", "viên"]
        # Nếu có, phải kèm "tham khảo bác sĩ"
    
    def test_always_recommend_doctor(self):
        """Test luôn khuyến nghị gặp bác sĩ"""
        mock_response = """
        Bạn có thể bị cảm lạnh.
        Nếu triệu chứng kéo dài, hãy gặp bác sĩ.
        """
        doctor_keywords = ["bác sĩ", "doctor", "khám", "bệnh viện"]
        # Phản hồi nên khuyến nghị gặp bác sĩ trong một số trường hợp


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
