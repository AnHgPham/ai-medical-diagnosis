"""
Medical AI Handler - Direct AI Diagnosis (No JSON Knowledge Base)
Handles all medical diagnosis using Gemini AI directly
"""
import os
import logging
from typing import List, Dict, Optional
import google.generativeai as genai

from config import (
    LLM_MODEL,
    LLM_TEMPERATURE,
    LLM_MAX_TOKENS,
    SYSTEM_PROMPT,
    EMERGENCY_KEYWORDS
)
from utils import setup_logging

logger = setup_logging(__name__)


class MedicalAIHandler:
    """Handle all medical diagnosis using AI directly"""
    
    def __init__(self, 
                 model_name: str = LLM_MODEL,
                 temperature: float = LLM_TEMPERATURE,
                 max_tokens: int = LLM_MAX_TOKENS):
        """Initialize Medical AI Handler"""
        self.model_name = model_name
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.model = None
        self.chat_session = None
        self.initialize_model()
    
    def initialize_model(self) -> None:
        """Initialize Gemini model with chat session"""
        try:
            # Get API key
            api_key = os.getenv("GEMINI_API_KEY")
            if not api_key:
                raise ValueError("GEMINI_API_KEY not found in environment variables")
            
            # Configure Gemini
            genai.configure(api_key=api_key)
            
            # Create model
            self.model = genai.GenerativeModel(
                model_name=self.model_name,
                generation_config={
                    "temperature": self.temperature,
                    "max_output_tokens": self.max_tokens,
                }
            )
            
            # Start chat session with system prompt as first message
            self.chat_session = self.model.start_chat(history=[
                {
                    'role': 'user',
                    'parts': [SYSTEM_PROMPT]
                },
                {
                    'role': 'model',
                    'parts': ['Tôi hiểu rồi. Tôi là AI Doctor và sẽ tuân thủ tất cả các quy tắc và hướng dẫn bạn đã đưa ra. Tôi sẵn sàng giúp đỡ người dùng với các vấn đề y tế của họ một cách chuyên nghiệp và an toàn.']
                }
            ])
            
            logger.info(f"Initialized Medical AI: {self.model_name}")
            
        except Exception as e:
            logger.error(f"Failed to initialize Medical AI: {e}")
            raise
    
    def check_emergency(self, user_input: str) -> Optional[str]:
        """Quick check for emergency keywords"""
        user_input_lower = user_input.lower()
        
        for keyword in EMERGENCY_KEYWORDS:
            if keyword in user_input_lower:
                return f"""
⚠️⚠️⚠️ **CẢNH BÁO KHẨN CẤP** ⚠️⚠️⚠️

Bạn đã đề cập đến triệu chứng **"{keyword}"** - đây có thể là dấu hiệu nghiêm trọng!

🚨 **HÀNH ĐỘNG NGAY LẬP TỨC:**
1. **Gọi cấp cứu 115** hoặc
2. **Đến bệnh viện gần nhất** ngay
3. **KHÔNG tự điều trị** tại nhà

Đây là tình huống khẩn cấp cần được xử lý bởi chuyên gia y tế ngay lập tức!

⏰ **THỜI GIAN LÀ VÀNG** - Đừng chần chừ!
"""
        
        return None
    
    def diagnose(self, user_input: str) -> str:
        """
        Main diagnosis function using AI directly
        No knowledge base needed - AI uses its full medical knowledge
        """
        try:
            logger.info("Processing diagnosis request")
            
            # Check for emergency first
            emergency_warning = self.check_emergency(user_input)
            if emergency_warning:
                logger.warning("Emergency symptoms detected")
                return emergency_warning
            
            # Send to AI for diagnosis
            response = self.chat_session.send_message(user_input)
            
            if not response or not response.text:
                logger.error("Empty response from AI")
                return "❌ Xin lỗi, tôi không thể tạo phản hồi lúc này. Vui lòng thử lại."
            
            logger.info("Successfully generated diagnosis")
            return response.text
            
        except Exception as e:
            logger.error(f"Error in diagnosis: {e}")
            return f"❌ Lỗi: {str(e)}\n\n💡 Vui lòng kiểm tra kết nối hoặc thử lại sau."
    
    def reset_conversation(self) -> None:
        """Reset chat session for new conversation"""
        try:
            # Reset with system prompt
            self.chat_session = self.model.start_chat(history=[
                {
                    'role': 'user',
                    'parts': [SYSTEM_PROMPT]
                },
                {
                    'role': 'model',
                    'parts': ['Tôi hiểu rồi. Tôi là AI Doctor và sẵn sàng giúp đỡ bạn.']
                }
            ])
            logger.info("Chat session reset")
        except Exception as e:
            logger.error(f"Error resetting conversation: {e}")
    
    def get_chat_history(self) -> List[Dict]:
        """Get current chat history"""
        try:
            if self.chat_session and hasattr(self.chat_session, 'history'):
                return [
                    {
                        'role': msg.role,
                        'content': msg.parts[0].text if msg.parts else ''
                    }
                    for msg in self.chat_session.history
                ]
            return []
        except Exception as e:
            logger.error(f"Error getting chat history: {e}")
            return []


# Export
__all__ = ['MedicalAIHandler']
