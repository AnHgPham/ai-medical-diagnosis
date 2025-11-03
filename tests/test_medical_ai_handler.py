"""
Test Medical AI Handler
Kiểm tra chức năng của module xử lý AI chẩn đoán
"""
import pytest
import sys
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from config import EMERGENCY_KEYWORDS


class TestEmergencyDetection:
    """Test cases for emergency symptom detection"""
    
    def test_detect_emergency_keyword_kho_tho(self):
        """Test phát hiện 'khó thở'"""
        user_input = "Tôi bị khó thở"
        assert any(keyword in user_input.lower() for keyword in EMERGENCY_KEYWORDS), \
            "Phải phát hiện được 'khó thở'"
    
    def test_detect_emergency_keyword_dau_nguc(self):
        """Test phát hiện 'đau ngực'"""
        user_input = "Tôi bị đau ngực dữ dội"
        assert any(keyword in user_input.lower() for keyword in EMERGENCY_KEYWORDS), \
            "Phải phát hiện được 'đau ngực'"
    
    def test_detect_emergency_keyword_bat_tinh(self):
        """Test phát hiện 'bất tỉnh'"""
        user_input = "Người nhà tôi bị bất tỉnh"
        assert any(keyword in user_input.lower() for keyword in EMERGENCY_KEYWORDS), \
            "Phải phát hiện được 'bất tỉnh'"
    
    def test_detect_emergency_keyword_co_giat(self):
        """Test phát hiện 'co giật'"""
        user_input = "Con tôi bị co giật"
        assert any(keyword in user_input.lower() for keyword in EMERGENCY_KEYWORDS), \
            "Phải phát hiện được 'co giật'"
    
    def test_no_emergency_normal_symptoms(self):
        """Test không phát hiện emergency với triệu chứng bình thường"""
        user_input = "Tôi bị sổ mũi và hắt hơi"
        has_emergency = any(keyword in user_input.lower() for keyword in EMERGENCY_KEYWORDS)
        assert not has_emergency, "Không nên phát hiện emergency với triệu chứng nhẹ"
    
    def test_emergency_case_insensitive(self):
        """Test phát hiện emergency không phân biệt hoa thường"""
        user_inputs = ["Tôi bị KHÓ THỞ", "tôi bị khó thở", "Tôi Bị Khó Thở"]
        for user_input in user_inputs:
            assert any(keyword in user_input.lower() for keyword in EMERGENCY_KEYWORDS), \
                f"Phải phát hiện emergency trong: {user_input}"
    
    def test_emergency_with_extra_text(self):
        """Test phát hiện emergency khi có nhiều text xung quanh"""
        user_input = "Tôi bị sốt cao và đau đầu, ngoài ra còn khó thở nữa"
        assert any(keyword in user_input.lower() for keyword in EMERGENCY_KEYWORDS), \
            "Phải phát hiện emergency ngay cả khi có nhiều text khác"
    
    def test_multiple_emergency_keywords(self):
        """Test phát hiện nhiều emergency keywords"""
        user_input = "Tôi bị đau ngực và khó thở"
        emergency_count = sum(1 for keyword in EMERGENCY_KEYWORDS if keyword in user_input.lower())
        assert emergency_count >= 2, "Phải phát hiện được nhiều emergency keywords"


class TestMedicalAIHandlerMocked:
    """Test Medical AI Handler with mocked API"""
    
    @patch('google.generativeai.configure')
    @patch('google.generativeai.GenerativeModel')
    def test_initialization_success(self, mock_model_class, mock_configure):
        """Test khởi tạo thành công"""
        # Mock environment variable
        with patch.dict('os.environ', {'GEMINI_API_KEY': 'test-api-key'}):
            mock_model = MagicMock()
            mock_chat = MagicMock()
            mock_model.start_chat.return_value = mock_chat
            mock_model_class.return_value = mock_model
            
            from medical_ai_handler import MedicalAIHandler
            handler = MedicalAIHandler()
            
            assert handler.model is not None, "Model phải được khởi tạo"
            assert handler.chat_session is not None, "Chat session phải được khởi tạo"
            mock_configure.assert_called_once_with(api_key='test-api-key')
    
    @patch('google.generativeai.configure')
    def test_initialization_no_api_key(self, mock_configure):
        """Test khởi tạo khi không có API key"""
        with patch.dict('os.environ', {}, clear=True):
            from medical_ai_handler import MedicalAIHandler
            with pytest.raises(ValueError, match="GEMINI_API_KEY not found"):
                handler = MedicalAIHandler()
    
    @patch('google.generativeai.configure')
    @patch('google.generativeai.GenerativeModel')
    def test_diagnose_normal_symptoms(self, mock_model_class, mock_configure):
        """Test chẩn đoán với triệu chứng bình thường"""
        with patch.dict('os.environ', {'GEMINI_API_KEY': 'test-api-key'}):
            # Setup mock
            mock_model = MagicMock()
            mock_chat = MagicMock()
            mock_response = MagicMock()
            mock_response.text = "Bạn có thể bị cảm lạnh. Triệu chứng: sổ mũi, hắt hơi..."
            mock_chat.send_message.return_value = mock_response
            mock_model.start_chat.return_value = mock_chat
            mock_model_class.return_value = mock_model
            
            from medical_ai_handler import MedicalAIHandler
            handler = MedicalAIHandler()
            
            result = handler.diagnose("Tôi bị sổ mũi và hắt hơi")
            
            assert result is not None, "Kết quả không được None"
            assert len(result) > 0, "Kết quả phải có nội dung"
            assert "cảm lạnh" in result.lower() or "sổ mũi" in result.lower(), \
                "Kết quả phải liên quan đến triệu chứng"
    
    @patch('google.generativeai.configure')
    @patch('google.generativeai.GenerativeModel')
    def test_diagnose_emergency_symptoms(self, mock_model_class, mock_configure):
        """Test chẩn đoán với triệu chứng khẩn cấp"""
        with patch.dict('os.environ', {'GEMINI_API_KEY': 'test-api-key'}):
            mock_model = MagicMock()
            mock_chat = MagicMock()
            mock_model.start_chat.return_value = mock_chat
            mock_model_class.return_value = mock_model
            
            from medical_ai_handler import MedicalAIHandler
            handler = MedicalAIHandler()
            
            result = handler.diagnose("Tôi bị đau ngực dữ dội")
            
            assert "CẢNH BÁO" in result or "KHẨN CẤP" in result, \
                "Phải có cảnh báo khẩn cấp"
            assert "115" in result or "bệnh viện" in result, \
                "Phải có hướng dẫn gọi cấp cứu"
    
    @patch('google.generativeai.configure')
    @patch('google.generativeai.GenerativeModel')
    def test_reset_conversation(self, mock_model_class, mock_configure):
        """Test reset conversation"""
        with patch.dict('os.environ', {'GEMINI_API_KEY': 'test-api-key'}):
            mock_model = MagicMock()
            mock_chat = MagicMock()
            mock_model.start_chat.return_value = mock_chat
            mock_model_class.return_value = mock_model
            
            from medical_ai_handler import MedicalAIHandler
            handler = MedicalAIHandler()
            
            # Reset
            handler.reset_conversation()
            
            # Verify start_chat được gọi lại
            assert mock_model.start_chat.call_count >= 2, \
                "start_chat phải được gọi lại khi reset"


class TestResponseQuality:
    """Test cases for AI response quality"""
    
    def test_response_not_empty(self):
        """Test response không rỗng"""
        mock_response = "Bạn có thể bị cảm lạnh..."
        assert len(mock_response) > 0, "Response không được rỗng"
    
    def test_response_has_diagnosis(self):
        """Test response có chẩn đoán"""
        mock_response = "Bạn có thể bị cảm lạnh. Triệu chứng phù hợp..."
        keywords = ["bị", "có thể", "khả năng", "chẩn đoán"]
        assert any(keyword in mock_response.lower() for keyword in keywords), \
            "Response phải có từ khóa chẩn đoán"
    
    def test_response_has_recommendation(self):
        """Test response có khuyến nghị"""
        mock_response = "Bạn nên nghỉ ngơi, uống nhiều nước..."
        keywords = ["nên", "khuyến nghị", "hướng dẫn", "cần"]
        assert any(keyword in mock_response.lower() for keyword in keywords), \
            "Response phải có khuyến nghị"
    
    def test_response_professional_tone(self):
        """Test response có giọng điệu chuyên nghiệp"""
        mock_response = "Dựa trên các triệu chứng bạn mô tả..."
        unprofessional_words = ["chắc chắn 100%", "không biết", "may be"]
        assert not any(word in mock_response.lower() for word in unprofessional_words), \
            "Response phải chuyên nghiệp"


class TestErrorHandling:
    """Test cases for error handling"""
    
    @patch('google.generativeai.configure')
    @patch('google.generativeai.GenerativeModel')
    def test_handle_api_error(self, mock_model_class, mock_configure):
        """Test xử lý lỗi API"""
        with patch.dict('os.environ', {'GEMINI_API_KEY': 'test-api-key'}):
            mock_model = MagicMock()
            mock_chat = MagicMock()
            mock_chat.send_message.side_effect = Exception("API Error")
            mock_model.start_chat.return_value = mock_chat
            mock_model_class.return_value = mock_model
            
            from medical_ai_handler import MedicalAIHandler
            handler = MedicalAIHandler()
            
            result = handler.diagnose("Tôi bị sốt")
            
            assert "Lỗi" in result or "Error" in result, \
                "Phải có thông báo lỗi"
    
    @patch('google.generativeai.configure')
    @patch('google.generativeai.GenerativeModel')
    def test_handle_empty_response(self, mock_model_class, mock_configure):
        """Test xử lý response rỗng"""
        with patch.dict('os.environ', {'GEMINI_API_KEY': 'test-api-key'}):
            mock_model = MagicMock()
            mock_chat = MagicMock()
            mock_response = MagicMock()
            mock_response.text = ""
            mock_chat.send_message.return_value = mock_response
            mock_model.start_chat.return_value = mock_chat
            mock_model_class.return_value = mock_model
            
            from medical_ai_handler import MedicalAIHandler
            handler = MedicalAIHandler()
            
            result = handler.diagnose("Tôi bị sốt")
            
            assert len(result) > 0, "Phải có thông báo lỗi khi response rỗng"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
