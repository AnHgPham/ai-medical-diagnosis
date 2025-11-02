"""
Medical LLM Handler for AI Medical Diagnosis System
Handles interactions with Google Gemini AI for medical diagnosis
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
    DIAGNOSIS_PROMPT_TEMPLATE
)
from utils import setup_logging

logger = setup_logging(__name__)


class MedicalLLMHandler:
    """Handle LLM interactions for medical diagnosis"""
    
    def __init__(self, 
                 model_name: str = LLM_MODEL,
                 temperature: float = LLM_TEMPERATURE,
                 max_tokens: int = LLM_MAX_TOKENS):
        """Initialize LLM handler"""
        self.model_name = model_name
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.model = None
        self.initialize_model()
    
    def initialize_model(self) -> None:
        """Initialize Gemini model"""
        try:
            # Get API key from environment or secrets
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
            
            logger.info(f"Initialized Gemini model: {self.model_name}")
            
        except Exception as e:
            logger.error(f"Failed to initialize Gemini model: {e}")
            raise
    
    def generate_diagnosis(self,
                          user_input: str,
                          knowledge_context: str,
                          chat_history: str = "",
                          symptoms_info: str = "") -> str:
        """Generate medical diagnosis response"""
        try:
            # Build prompt
            prompt = DIAGNOSIS_PROMPT_TEMPLATE.format(
                user_input=user_input,
                knowledge_context=knowledge_context,
                chat_history=chat_history if chat_history else "Chưa có lịch sử",
                symptoms_info=symptoms_info if symptoms_info else "Chưa có triệu chứng được xác định"
            )
            
            # Add system prompt
            full_prompt = f"{SYSTEM_PROMPT}\n\n{prompt}"
            
            logger.info("Generating diagnosis response")
            logger.debug(f"Prompt length: {len(full_prompt)} characters")
            
            # Generate response
            response = self.model.generate_content(full_prompt)
            
            if not response or not response.text:
                logger.error("Empty response from model")
                return "❌ Xin lỗi, tôi không thể tạo phản hồi lúc này. Vui lòng thử lại."
            
            logger.info("Successfully generated diagnosis response")
            return response.text
            
        except Exception as e:
            logger.error(f"Error generating diagnosis: {e}")
            return f"❌ Lỗi: {str(e)}\n\n💡 Vui lòng kiểm tra API key hoặc thử lại sau."
    
    def generate_follow_up_questions(self,
                                    current_symptoms: List[str],
                                    possible_diseases: List[Dict]) -> str:
        """Generate follow-up questions to narrow down diagnosis"""
        try:
            prompt = f"""Dựa trên các triệu chứng hiện tại:
{', '.join(current_symptoms)}

Và các bệnh có thể:
{', '.join([d['name'] for d in possible_diseases[:3]])}

Hãy đặt 2-3 câu hỏi bổ sung để xác định chính xác hơn tình trạng sức khỏe.
Câu hỏi nên:
- Cụ thể và dễ trả lời
- Giúp phân biệt giữa các bệnh
- Liên quan đến mức độ, thời gian, hoặc triệu chứng đi kèm
"""
            
            response = self.model.generate_content(prompt)
            return response.text if response and response.text else ""
            
        except Exception as e:
            logger.error(f"Error generating follow-up questions: {e}")
            return ""
    
    def assess_severity(self, symptoms: List[str]) -> Dict:
        """Assess severity of symptoms"""
        try:
            prompt = f"""Đánh giá mức độ nghiêm trọng của các triệu chứng sau:
{', '.join(symptoms)}

Trả lời theo format JSON:
{{
    "severity_level": "mild/moderate/severe/critical",
    "urgency": "can_wait/should_see_doctor_soon/emergency",
    "explanation": "Giải thích ngắn gọn"
}}
"""
            
            response = self.model.generate_content(prompt)
            
            if response and response.text:
                # Try to parse JSON response
                import json
                try:
                    return json.loads(response.text)
                except:
                    # Fallback to text response
                    return {
                        "severity_level": "unknown",
                        "urgency": "should_see_doctor_soon",
                        "explanation": response.text
                    }
            
            return {
                "severity_level": "unknown",
                "urgency": "should_see_doctor_soon",
                "explanation": "Không thể đánh giá"
            }
            
        except Exception as e:
            logger.error(f"Error assessing severity: {e}")
            return {
                "severity_level": "unknown",
                "urgency": "should_see_doctor_soon",
                "explanation": str(e)
            }
    
    def generate_treatment_recommendations(self, 
                                          diagnosis: str,
                                          symptoms: List[str]) -> str:
        """Generate treatment recommendations"""
        try:
            prompt = f"""Dựa trên chẩn đoán: {diagnosis}
Và các triệu chứng: {', '.join(symptoms)}

Hãy đưa ra khuyến nghị điều trị bao gồm:
1. Các bước tự chăm sóc tại nhà
2. Thuốc không kê đơn có thể dùng (nếu phù hợp)
3. Khi nào cần gặp bác sĩ
4. Các lưu ý quan trọng

Lưu ý: Luôn nhắc nhở đây chỉ là tham khảo, cần tham khảo bác sĩ.
"""
            
            response = self.model.generate_content(prompt)
            return response.text if response and response.text else ""
            
        except Exception as e:
            logger.error(f"Error generating treatment recommendations: {e}")
            return ""
    
    def format_medical_response(self,
                               diagnosis_text: str,
                               confidence: float = None,
                               matched_diseases: List[Dict] = None) -> str:
        """Format medical response with structure"""
        formatted = diagnosis_text
        
        # Add confidence if available
        if confidence is not None:
            formatted += f"\n\n**Độ tin cậy:** {confidence*100:.1f}%"
        
        # Add matched diseases if available
        if matched_diseases:
            formatted += "\n\n**Các bệnh có thể:**\n"
            for i, disease_info in enumerate(matched_diseases[:3], 1):
                disease = disease_info['disease']
                score = disease_info.get('score', 0)
                formatted += f"{i}. {disease['name']} (Khớp: {score*100:.0f}%)\n"
        
        return formatted
    
    def check_emergency_symptoms(self, symptoms: List[str]) -> Optional[str]:
        """Check for emergency symptoms"""
        emergency_keywords = [
            'khó thở', 'đau ngực', 'bất tỉnh', 'co giật', 
            'chảy máu nhiều', 'đau đầu dữ dội', 'liệt',
            'mất ý thức', 'sốc', 'ngộ độc'
        ]
        
        symptoms_text = ' '.join(symptoms).lower()
        
        for keyword in emergency_keywords:
            if keyword in symptoms_text:
                return f"""
⚠️⚠️⚠️ **CẢNH BÁO KHẨN CẤP** ⚠️⚠️⚠️

Triệu chứng "{keyword}" có thể là dấu hiệu nghiêm trọng!

🚨 **HÀNH ĐỘNG NGAY:**
- Gọi cấp cứu 115
- Đến bệnh viện gần nhất
- KHÔNG tự điều trị tại nhà

Đây là tình huống khẩn cấp cần được xử lý ngay lập tức!
"""
        
        return None


# Export
__all__ = ['MedicalLLMHandler']
