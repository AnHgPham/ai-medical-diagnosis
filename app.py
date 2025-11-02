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

from config import APP_TITLE, APP_ICON, WARNING_MESSAGE
from medical_ai_handler import MedicalAIHandler
from utils import setup_logging

# Setup logging
logger = setup_logging(__name__)

# Page configuration
st.set_page_config(
    page_title="AI Medical Diagnosis",
    page_icon=APP_ICON,
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom CSS - Clean and Professional
st.markdown("""
<style>
    /* Global */
    .main {
        background: #f5f7fa;
    }
    
    /* Header */
    .header-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        color: white;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .header-container h1 {
        font-size: 2.2rem;
        font-weight: 700;
        margin: 0;
    }
    
    .header-container p {
        font-size: 1rem;
        margin: 0.5rem 0 0 0;
        opacity: 0.95;
    }
    
    /* Warning */
    .warning-container {
        background: #fff3cd;
        border-left: 4px solid #ff9800;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    /* Chat messages */
    .user-msg {
        background: #e3f2fd;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.8rem 0;
        border-left: 4px solid #2196f3;
    }
    
    .ai-msg {
        background: #f3e5f5;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.8rem 0;
        border-left: 4px solid #9c27b0;
    }
    
    .msg-header {
        display: flex;
        justify-content: space-between;
        margin-bottom: 0.5rem;
        font-weight: 600;
    }
    
    .msg-time {
        font-size: 0.85rem;
        color: #666;
        font-weight: normal;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    
    /* Buttons */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.6rem 1.5rem;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }
</style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Initialize session state"""
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    if 'ai_handler' not in st.session_state:
        try:
            st.session_state.ai_handler = MedicalAIHandler()
            logger.info("AI Handler initialized")
        except Exception as e:
            logger.error(f"Failed to initialize AI: {e}")
            st.error(f"❌ Lỗi khởi tạo AI: {str(e)}")
            st.stop()


def display_message(role, content, timestamp=""):
    """Display a chat message"""
    if role == 'user':
        st.markdown(f"""
        <div class="user-msg">
            <div class="msg-header">
                <span>👤 Bạn</span>
                <span class="msg-time">{timestamp}</span>
            </div>
            <div>{content.replace('<', '&lt;').replace('>', '&gt;')}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="ai-msg">
            <div class="msg-header">
                <span>🏥 AI Doctor</span>
                <span class="msg-time">{timestamp}</span>
            </div>
            <div>{content.replace('<', '&lt;').replace('>', '&gt;')}</div>
        </div>
        """, unsafe_allow_html=True)


def main():
    """Main application"""
    
    # Initialize
    initialize_session_state()
    
    # Header
    st.markdown("""
    <div class="header-container">
        <h1>🏥 AI Medical Diagnosis</h1>
        <p>Hệ thống Chẩn đoán Y tế Thông minh | Powered by Google Gemini AI</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Warning
    st.warning(WARNING_MESSAGE)
    
    # Sidebar
    with st.sidebar:
        st.title("🎯 AI Doctor")
        
        st.markdown("---")
        
        st.markdown("### 💡 Khả năng của AI")
        st.markdown("""
        - 🌍 **Kiến thức toàn diện** về hàng ngàn bệnh lý
        - 🔍 **Phân tích thông minh** các triệu chứng
        - 💊 **Chẩn đoán chính xác** dựa trên AI
        - ⚠️ **Cảnh báo kịp thời** các dấu hiệu nguy hiểm
        - 💬 **Tư vấn 24/7** luôn sẵn sàng
        """)
        
        st.markdown("---")
        
        st.markdown("### 🔧 Công nghệ")
        st.markdown("""
        - **AI Model:** Google Gemini 2.0 Flash
        - **Framework:** Streamlit
        - **Approach:** AI-Direct Diagnosis
        - **Language:** Python 3.11
        """)
        
        st.markdown("---")
        
        # Reset button
        if st.button("🗑️ Xóa lịch sử chat"):
            st.session_state.messages = []
            st.session_state.ai_handler.reset_conversation()
            st.success("✅ Đã xóa lịch sử chat!")
            st.rerun()
        

    
    # Main chat area
    st.markdown("## 💬 Chat với AI Doctor")
    
    # Display greeting if no messages
    if not st.session_state.messages:
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
        display_message('assistant', greeting)
    
    # Display chat history
    for msg in st.session_state.messages:
        display_message(
            msg['role'],
            msg['content'],
            msg.get('timestamp', '')
        )
    
    # Chat input
    user_input = st.chat_input("💬 Mô tả triệu chứng của bạn...")
    
    if user_input:
        timestamp = datetime.now().strftime("%H:%M")
        
        # Add user message
        st.session_state.messages.append({
            'role': 'user',
            'content': user_input,
            'timestamp': timestamp
        })
        
        # Get AI response
        with st.spinner("🔍 AI Doctor đang phân tích..."):
            try:
                ai_response = st.session_state.ai_handler.diagnose(user_input)
                
                st.session_state.messages.append({
                    'role': 'assistant',
                    'content': ai_response,
                    'timestamp': timestamp
                })
                
                logger.info("Successfully processed user input")
                
            except Exception as e:
                logger.error(f"Error: {e}")
                error_msg = f"❌ Lỗi: {str(e)}\n\n💡 Vui lòng thử lại sau."
                st.session_state.messages.append({
                    'role': 'assistant',
                    'content': error_msg,
                    'timestamp': timestamp
                })
        
        st.rerun()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 1rem;">
        © 2025 AI Medical Diagnosis System | Powered by <b>Google Gemini AI</b><br>
        <a href="https://github.com/AnHgPham/ai-medical-diagnosis" target="_blank" style="color: #667eea;">GitHub</a> • 
        <a href="https://streamlit.io" target="_blank" style="color: #667eea;">Streamlit</a> • 
        <a href="https://ai.google.dev/" target="_blank" style="color: #667eea;">Google AI</a>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
