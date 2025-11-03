"""
Test Integration
Kiểm tra tích hợp các module và luồng hoạt động tổng thể
"""
import pytest
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))


class TestEndToEndFlow:
    """Test luồng hoạt động từ đầu đến cuối"""
    
    @patch('google.generativeai.configure')
    @patch('google.generativeai.GenerativeModel')
    def test_normal_diagnosis_flow(self, mock_model_class, mock_configure):
        """Test luồng chẩn đoán bình thường"""
        with patch.dict('os.environ', {'GEMINI_API_KEY': 'test-api-key'}):
            # Setup mock
            mock_model = MagicMock()
            mock_chat = MagicMock()
            mock_response = MagicMock()
            mock_response.text = "Bạn có thể bị cảm lạnh. Khuyến nghị: nghỉ ngơi, uống nhiều nước."
            mock_chat.send_message.return_value = mock_response
            mock_model.start_chat.return_value = mock_chat
            mock_model_class.return_value = mock_model
            
            from medical_ai_handler import MedicalAIHandler
            
            # 1. Khởi tạo handler
            handler = MedicalAIHandler()
            assert handler is not None
            
            # 2. Người dùng nhập triệu chứng
            user_input = "Tôi bị sổ mũi và hắt hơi"
            
            # 3. Validate input
            assert len(user_input.strip()) > 0
            
            # 4. Gọi diagnose
            result = handler.diagnose(user_input)
            
            # 5. Kiểm tra kết quả
            assert result is not None
            assert len(result) > 0
            assert "cảm lạnh" in result.lower()
    
    @patch('google.generativeai.configure')
    @patch('google.generativeai.GenerativeModel')
    def test_emergency_flow(self, mock_model_class, mock_configure):
        """Test luồng xử lý khẩn cấp"""
        with patch.dict('os.environ', {'GEMINI_API_KEY': 'test-api-key'}):
            mock_model = MagicMock()
            mock_chat = MagicMock()
            mock_model.start_chat.return_value = mock_chat
            mock_model_class.return_value = mock_model
            
            from medical_ai_handler import MedicalAIHandler
            
            # 1. Khởi tạo handler
            handler = MedicalAIHandler()
            
            # 2. Người dùng nhập triệu chứng khẩn cấp
            user_input = "Tôi bị đau ngực dữ dội"
            
            # 3. Gọi diagnose
            result = handler.diagnose(user_input)
            
            # 4. Phải có cảnh báo khẩn cấp
            assert "CẢNH BÁO" in result or "KHẨN CẤP" in result
            assert "115" in result or "bệnh viện" in result
    
    @patch('google.generativeai.configure')
    @patch('google.generativeai.GenerativeModel')
    def test_conversation_flow(self, mock_model_class, mock_configure):
        """Test luồng hội thoại nhiều lượt"""
        with patch.dict('os.environ', {'GEMINI_API_KEY': 'test-api-key'}):
            mock_model = MagicMock()
            mock_chat = MagicMock()
            
            # Mock responses cho nhiều lượt
            responses = [
                "Sốt của bạn cao bao nhiêu độ?",
                "Sốt 39 độ là khá cao. Bạn có triệu chứng nào khác không?",
                "Có thể là cúm. Khuyến nghị: nghỉ ngơi, uống nhiều nước."
            ]
            
            mock_chat.send_message.side_effect = [
                MagicMock(text=resp) for resp in responses
            ]
            
            mock_model.start_chat.return_value = mock_chat
            mock_model_class.return_value = mock_model
            
            from medical_ai_handler import MedicalAIHandler
            handler = MedicalAIHandler()
            
            # Lượt 1
            result1 = handler.diagnose("Tôi bị sốt")
            assert "bao nhiêu" in result1.lower()
            
            # Lượt 2
            result2 = handler.diagnose("39 độ")
            assert "39" in result2 or "cao" in result2.lower()
            
            # Lượt 3
            result3 = handler.diagnose("Tôi còn bị ho và đau đầu")
            assert len(result3) > 0


class TestModuleIntegration:
    """Test tích hợp giữa các module"""
    
    def test_config_import(self):
        """Test import config module"""
        from config import (
            LLM_MODEL,
            LLM_TEMPERATURE,
            LLM_MAX_TOKENS,
            SYSTEM_PROMPT,
            EMERGENCY_KEYWORDS
        )
        
        assert LLM_MODEL is not None
        assert isinstance(LLM_TEMPERATURE, (int, float))
        assert isinstance(LLM_MAX_TOKENS, int)
        assert len(SYSTEM_PROMPT) > 0
        assert len(EMERGENCY_KEYWORDS) > 0
    
    def test_utils_import(self):
        """Test import utils module"""
        from utils import setup_logging
        
        logger = setup_logging("test")
        assert logger is not None
    
    @patch('google.generativeai.configure')
    @patch('google.generativeai.GenerativeModel')
    def test_handler_uses_config(self, mock_model_class, mock_configure):
        """Test handler sử dụng config đúng cách"""
        with patch.dict('os.environ', {'GEMINI_API_KEY': 'test-api-key'}):
            mock_model = MagicMock()
            mock_chat = MagicMock()
            mock_model.start_chat.return_value = mock_chat
            mock_model_class.return_value = mock_model
            
            from medical_ai_handler import MedicalAIHandler
            from config import LLM_MODEL, LLM_TEMPERATURE, LLM_MAX_TOKENS
            
            handler = MedicalAIHandler()
            
            # Verify sử dụng config
            assert handler.model_name == LLM_MODEL
            assert handler.temperature == LLM_TEMPERATURE
            assert handler.max_tokens == LLM_MAX_TOKENS


class TestErrorRecovery:
    """Test khả năng phục hồi lỗi"""
    
    @patch('google.generativeai.configure')
    @patch('google.generativeai.GenerativeModel')
    def test_recover_from_api_error(self, mock_model_class, mock_configure):
        """Test phục hồi từ lỗi API"""
        with patch.dict('os.environ', {'GEMINI_API_KEY': 'test-api-key'}):
            mock_model = MagicMock()
            mock_chat = MagicMock()
            
            # Lần đầu lỗi, lần sau thành công
            mock_chat.send_message.side_effect = [
                Exception("API Error"),
                MagicMock(text="Bạn có thể bị cảm lạnh")
            ]
            
            mock_model.start_chat.return_value = mock_chat
            mock_model_class.return_value = mock_model
            
            from medical_ai_handler import MedicalAIHandler
            handler = MedicalAIHandler()
            
            # Lần 1: Lỗi
            result1 = handler.diagnose("Tôi bị sốt")
            assert "Lỗi" in result1
            
            # Lần 2: Thành công
            result2 = handler.diagnose("Tôi bị sốt")
            assert "cảm lạnh" in result2.lower()
    
    @patch('google.generativeai.configure')
    @patch('google.generativeai.GenerativeModel')
    def test_reset_after_error(self, mock_model_class, mock_configure):
        """Test reset sau khi gặp lỗi"""
        with patch.dict('os.environ', {'GEMINI_API_KEY': 'test-api-key'}):
            mock_model = MagicMock()
            mock_chat = MagicMock()
            mock_model.start_chat.return_value = mock_chat
            mock_model_class.return_value = mock_model
            
            from medical_ai_handler import MedicalAIHandler
            handler = MedicalAIHandler()
            
            # Reset không nên gây lỗi
            handler.reset_conversation()
            
            # Vẫn hoạt động bình thường sau reset
            assert handler.chat_session is not None


class TestPerformance:
    """Test hiệu năng"""
    
    @patch('google.generativeai.configure')
    @patch('google.generativeai.GenerativeModel')
    def test_initialization_time(self, mock_model_class, mock_configure):
        """Test thời gian khởi tạo"""
        import time
        
        with patch.dict('os.environ', {'GEMINI_API_KEY': 'test-api-key'}):
            mock_model = MagicMock()
            mock_chat = MagicMock()
            mock_model.start_chat.return_value = mock_chat
            mock_model_class.return_value = mock_model
            
            from medical_ai_handler import MedicalAIHandler
            
            start = time.time()
            handler = MedicalAIHandler()
            end = time.time()
            
            # Khởi tạo phải nhanh (< 1 giây với mock)
            assert (end - start) < 1.0
    
    @patch('google.generativeai.configure')
    @patch('google.generativeai.GenerativeModel')
    def test_emergency_check_speed(self, mock_model_class, mock_configure):
        """Test tốc độ kiểm tra emergency"""
        import time
        
        with patch.dict('os.environ', {'GEMINI_API_KEY': 'test-api-key'}):
            mock_model = MagicMock()
            mock_chat = MagicMock()
            mock_model.start_chat.return_value = mock_chat
            mock_model_class.return_value = mock_model
            
            from medical_ai_handler import MedicalAIHandler
            handler = MedicalAIHandler()
            
            start = time.time()
            result = handler.check_emergency("Tôi bị đau ngực")
            end = time.time()
            
            # Emergency check phải rất nhanh (< 0.1 giây)
            assert (end - start) < 0.1


class TestDataFlow:
    """Test luồng dữ liệu"""
    
    @patch('google.generativeai.configure')
    @patch('google.generativeai.GenerativeModel')
    def test_input_to_output_flow(self, mock_model_class, mock_configure):
        """Test luồng từ input đến output"""
        with patch.dict('os.environ', {'GEMINI_API_KEY': 'test-api-key'}):
            mock_model = MagicMock()
            mock_chat = MagicMock()
            mock_response = MagicMock()
            mock_response.text = "Test response"
            mock_chat.send_message.return_value = mock_response
            mock_model.start_chat.return_value = mock_chat
            mock_model_class.return_value = mock_model
            
            from medical_ai_handler import MedicalAIHandler
            handler = MedicalAIHandler()
            
            # Input
            user_input = "Tôi bị sốt"
            
            # Process
            result = handler.diagnose(user_input)
            
            # Output
            assert isinstance(result, str)
            assert len(result) > 0
    
    @patch('google.generativeai.configure')
    @patch('google.generativeai.GenerativeModel')
    def test_chat_history_persistence(self, mock_model_class, mock_configure):
        """Test lưu trữ lịch sử chat"""
        with patch.dict('os.environ', {'GEMINI_API_KEY': 'test-api-key'}):
            mock_model = MagicMock()
            mock_chat = MagicMock()
            mock_chat.history = []
            mock_chat.send_message.return_value = MagicMock(text="Response")
            mock_model.start_chat.return_value = mock_chat
            mock_model_class.return_value = mock_model
            
            from medical_ai_handler import MedicalAIHandler
            handler = MedicalAIHandler()
            
            # Gửi nhiều tin nhắn
            handler.diagnose("Tin nhắn 1")
            handler.diagnose("Tin nhắn 2")
            
            # Lịch sử phải được lưu
            history = handler.get_chat_history()
            assert isinstance(history, list)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
