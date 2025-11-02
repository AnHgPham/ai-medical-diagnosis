"""
AI Medical Diagnosis System - Streamlit Application
AI-Direct Approach (No JSON Knowledge Base)
"""
import streamlit as st
import sys
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from config import (
    APP_TITLE,
    APP_ICON,
    WARNING_MESSAGE
)
from medical_ai_handler import MedicalAIHandler
from utils import setup_logging

# Setup logging
logger = setup_logging(__name__)

# Page configuration
st.set_page_config(
    page_title="AI Medical Diagnosis",
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - Modern and Clean
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main container */
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* Header */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2.5rem;
        border-radius: 20px;
        text-align: center;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
    }
    
    .main-header h1 {
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    
    .main-header p {
        font-size: 1.2rem;
        opacity: 0.95;
        font-weight: 300;
    }
    
    /* Warning box */
    .warning-box {
        background: linear-gradient(135deg, #fff3cd 0%, #ffe69c 100%);
        border-left: 5px solid #ff9800;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1.5rem 0;
        box-shadow: 0 4px 15px rgba(255, 152, 0, 0.2);
    }
    
    .warning-box strong {
        color: #e65100;
        font-size: 1.1rem;
    }
    
    /* Chat container */
    .chat-container {
        background: white;
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        margin: 1rem 0;
        min-height: 400px;
    }
    
    /* Chat messages */
    .user-message {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        padding: 1.2rem;
        border-radius: 15px;
        margin: 1rem 0;
        border-left: 5px solid #2196f3;
        box-shadow: 0 3px 10px rgba(33, 150, 243, 0.2);
        animation: slideInRight 0.3s ease-out;
    }
    
    .ai-message {
        background: linear-gradient(135deg, #f3e5f5 0%, #e1bee7 100%);
        padding: 1.2rem;
        border-radius: 15px;
        margin: 1rem 0;
        border-left: 5px solid #9c27b0;
        box-shadow: 0 3px 10px rgba(156, 39, 176, 0.2);
        animation: slideInLeft 0.3s ease-out;
    }
    
    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(30px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes slideInLeft {
        from {
            opacity: 0;
            transform: translateX(-30px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    /* Sidebar */
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Info cards */
    .info-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        border: 1px solid #e0e0e0;
    }
    
    .info-card h4 {
        color: #667eea;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    
    .info-card ul {
        list-style: none;
        padding-left: 0;
    }
    
    .info-card li {
        padding: 0.5rem 0;
        border-bottom: 1px solid #f0f0f0;
    }
    
    .info-card li:last-child {
        border-bottom: none;
    }
    
    /* Feature badge */
    .feature-badge {
        display: inline-block;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: 600;
        margin: 0.3rem;
        box-shadow: 0 3px 10px rgba(102, 126, 234, 0.3);
    }
    
    /* Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.8rem 2rem;
        border-radius: 25px;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }
    
    /* Chat input */
    .stChatInput {
        border-radius: 25px;
        border: 2px solid #667eea;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem;
        color: #666;
        font-size: 0.9rem;
        margin-top: 3rem;
    }
    
    .footer a {
        color: #667eea;
        text-decoration: none;
        font-weight: 600;
    }
    
    .footer a:hover {
        text-decoration: underline;
    }
</style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Initialize session state variables"""
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    if 'ai_handler' not in st.session_state:
        try:
            st.session_state.ai_handler = MedicalAIHandler()
            logger.info("AI Handler initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize AI Handler: {e}")
            st.error(f"❌ Lỗi khởi tạo AI: {str(e)}")
            st.stop()


def display_greeting():
    """Display initial greeting message"""
    greeting = """
👋 **Xin chào! Tôi là AI Doctor - Trợ lý Y tế Thông minh**

Tôi được trang bị kiến thức y khoa toàn diện và có thể giúp bạn:

🔍 **Phân tích triệu chứng** - Hiểu rõ các dấu hiệu bệnh lý  
💊 **Chẩn đoán sơ bộ** - Đưa ra các khả năng bệnh với độ tin cậy  
💡 **Khuyến nghị điều trị** - Hướng dẫn chăm sóc và điều trị phù hợp  
⚠️ **Cảnh báo nguy hiểm** - Nhận biết triệu chứng cần cấp cứu ngay  

---

**Hãy mô tả triệu chứng của bạn, tôi sẽ đặt câu hỏi để hiểu rõ hơn!**

_Ví dụ: "Tôi bị sốt 39 độ từ 2 ngày nay, ho nhiều và đau đầu"_

---

⚠️ **Lưu ý**: Đây chỉ là tham khảo, luôn tham khảo bác sĩ chuyên khoa khi cần!
"""
    
    st.markdown(f"""
    <div class="ai-message">
        {greeting}
    </div>
    """, unsafe_allow_html=True)


def main():
    """Main application"""
    
    # Initialize session state
    initialize_session_state()
    
    # Header
    st.markdown(f"""
    <div class="main-header">
        <h1>🏥 AI Medical Diagnosis</h1>
        <p>Hệ thống Chẩn đoán Y tế Thông minh | Powered by Google Gemini AI</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Warning
    st.markdown(f"""
    <div class="warning-box">
        {WARNING_MESSAGE}
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("### 🎯 Tính năng AI Doctor")
        
        st.markdown("""
        <div class="info-card">
            <h4>💡 Khả năng của AI</h4>
            <ul>
                <li>🌍 <b>Kiến thức toàn diện</b> - Hàng ngàn bệnh lý</li>
                <li>🔍 <b>Phân tích thông minh</b> - Đặt câu hỏi chi tiết</li>
                <li>💊 <b>Chẩn đoán chính xác</b> - Dựa trên triệu chứng</li>
                <li>⚠️ <b>Cảnh báo kịp thời</b> - Nhận biết nguy hiểm</li>
                <li>💬 <b>Tư vấn 24/7</b> - Luôn sẵn sàng hỗ trợ</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        st.markdown("""
        <div class="info-card">
            <h4>🔧 Công nghệ</h4>
            <ul>
                <li><b>AI Model:</b> Google Gemini 2.0 Flash</li>
                <li><b>Framework:</b> Streamlit</li>
                <li><b>Approach:</b> AI-Direct Diagnosis</li>
                <li><b>Language:</b> Python 3.11</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Clear chat button
        if st.button("🗑️ Xóa lịch sử chat", use_container_width=True):
            st.session_state.messages = []
            st.session_state.ai_handler.reset_conversation()
            st.rerun()
        
        st.markdown("---")
        
        st.markdown("""
        <div style="text-align: center; padding: 1rem;">
            <p style="font-size: 0.9rem; color: #666;">
                Made with ❤️ by AnHgPham<br>
                <a href="https://github.com/AnHgPham/ai-medical-diagnosis" target="_blank" style="color: #667eea;">
                    View on GitHub
                </a>
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Main chat area
    st.markdown("### 💬 Chat với AI Doctor")
    
    # Chat container
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    # Display greeting if no messages
    if not st.session_state.messages:
        display_greeting()
    
    # Display chat history
    for message in st.session_state.messages:
        role = message['role']
        content = message['content']
        timestamp = message.get('timestamp', '')
        
        if role == 'user':
            st.markdown(f"""
            <div class="user-message">
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                    <b>👤 Bạn</b>
                    <span style="font-size: 0.8rem; color: #666;">{timestamp}</span>
                </div>
                <div>{content}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="ai-message">
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                    <b>🏥 AI Doctor</b>
                    <span style="font-size: 0.8rem; color: #666;">{timestamp}</span>
                </div>
                <div>{content}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Chat input
    user_input = st.chat_input("💬 Mô tả triệu chứng của bạn... (Ví dụ: Tôi bị sốt cao, ho và đau đầu)")
    
    if user_input:
        # Get current timestamp
        timestamp = datetime.now().strftime("%H:%M")
        
        # Add user message
        st.session_state.messages.append({
            'role': 'user',
            'content': user_input,
            'timestamp': timestamp
        })
        
        # Show processing
        with st.spinner("🔍 AI Doctor đang phân tích triệu chứng của bạn..."):
            try:
                # Get AI diagnosis
                ai_response = st.session_state.ai_handler.diagnose(user_input)
                
                # Add AI response
                st.session_state.messages.append({
                    'role': 'assistant',
                    'content': ai_response,
                    'timestamp': timestamp
                })
                
                logger.info("Successfully processed user input")
                
            except Exception as e:
                logger.error(f"Error processing user input: {e}")
                error_message = f"❌ Lỗi: {str(e)}\n\n💡 Vui lòng thử lại sau."
                st.session_state.messages.append({
                    'role': 'assistant',
                    'content': error_message,
                    'timestamp': timestamp
                })
        
        # Rerun to show new messages
        st.rerun()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div class="footer">
        © 2025 AI Medical Diagnosis System | Powered by <b>Google Gemini AI</b><br>
        <a href="https://github.com/AnHgPham/ai-medical-diagnosis" target="_blank">GitHub</a> • 
        <a href="https://streamlit.io" target="_blank">Streamlit</a> • 
        <a href="https://ai.google.dev/" target="_blank">Google AI</a>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
