"""
AI Medical Diagnosis System - Streamlit Application
Main UI application using modular architecture
"""
import streamlit as st
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from config import (
    APP_TITLE,
    APP_ICON,
    SIDEBAR_TITLE,
    WARNING_MESSAGE
)
from knowledge_manager import KnowledgeManager
from medical_llm_handler import MedicalLLMHandler
from diagnosis_engine import DiagnosisEngine
from utils import SessionManager, setup_logging, sanitize_user_input, format_timestamp

# Setup logging
logger = setup_logging(__name__)

# Page configuration
st.set_page_config(
    page_title="AI Medical Diagnosis",
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    /* Main header */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        text-align: center;
        color: white;
        margin-bottom: 2rem;
    }
    
    .main-header h1 {
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    
    .main-header p {
        font-size: 1.1rem;
        opacity: 0.9;
    }
    
    /* Stats cards */
    .stats-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        color: white;
        margin-bottom: 1rem;
    }
    
    .stats-card h2 {
        font-size: 2.5rem;
        font-weight: bold;
        margin: 0;
    }
    
    .stats-card p {
        font-size: 1rem;
        margin: 0.5rem 0 0 0;
        opacity: 0.9;
    }
    
    /* Warning box */
    .warning-box {
        background-color: #fff3cd;
        border-left: 4px solid #ffc107;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    
    /* Chat messages */
    .user-message {
        background-color: #e3f2fd;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid #2196f3;
    }
    
    .ai-message {
        background: linear-gradient(to right, #f8f9fa, #e9ecef);
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid #667eea;
    }
    
    /* Info card */
    .info-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
    }
    
    /* Button styling */
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.5rem 2rem;
        border-radius: 25px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(102, 126, 234, 0.4);
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def initialize_system():
    """Initialize system components"""
    try:
        logger.info("Initializing system components")
        
        # Initialize knowledge manager
        knowledge_manager = KnowledgeManager()
        
        # Initialize LLM handler
        llm_handler = MedicalLLMHandler()
        
        # Initialize diagnosis engine
        diagnosis_engine = DiagnosisEngine(knowledge_manager, llm_handler)
        
        logger.info("System initialized successfully")
        return knowledge_manager, llm_handler, diagnosis_engine
        
    except Exception as e:
        logger.error(f"Failed to initialize system: {e}")
        st.error(f"❌ Lỗi khởi tạo hệ thống: {str(e)}")
        st.stop()


def main():
    """Main application"""
    
    # Initialize system
    knowledge_manager, llm_handler, diagnosis_engine = initialize_system()
    
    # Initialize session state
    SessionManager.initialize_session(st.session_state)
    
    # Header
    st.markdown(f"""
    <div class="main-header">
        <h1>{APP_ICON} AI Medical Diagnosis System</h1>
        <p>Hệ thống chẩn đoán y tế thông minh được hỗ trợ bởi Google Gemini AI</p>
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
        st.markdown(f"### {SIDEBAR_TITLE}")
        
        # Get statistics
        stats = knowledge_manager.get_statistics()
        
        # Stats cards
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            <div class="stats-card">
                <h2>{stats['total_diseases']}</h2>
                <p>Bệnh phổ biến</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="stats-card">
                <h2>{stats['total_symptoms']}</h2>
                <p>Triệu chứng</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Info card
        st.markdown("""
        <div class="info-card">
            <h4>🎯 Tính năng</h4>
            <ul>
                <li>💬 Chat với AI Doctor</li>
                <li>🧠 Phân tích thông minh</li>
                <li>📊 Chẩn đoán chi tiết</li>
                <li>💊 Khuyến nghị điều trị</li>
                <li>⚠️ Cảnh báo nguy hiểm</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # System info
        st.markdown("""
        <div class="info-card">
            <h4>🔧 Công nghệ</h4>
            <ul>
                <li><b>AI Model:</b> Google Gemini Pro</li>
                <li><b>Framework:</b> Streamlit</li>
                <li><b>Language:</b> Python 3.11</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # Clear chat button
        if st.button("🗑️ Xóa lịch sử chat"):
            st.session_state.messages = []
            st.session_state.chat_history = []
            st.session_state.user_symptoms = []
            st.rerun()
    
    # Main chat area
    st.markdown("### 💬 Chat với AI Doctor")
    
    # Display greeting if no messages
    if not st.session_state.messages:
        greeting = """
        👋 **Xin chào! Tôi là AI Doctor, trợ lý y tế thông minh.**
        
        Tôi có thể giúp bạn:
        - 🔍 Phân tích các triệu chứng bạn đang gặp phải
        - 💡 Đưa ra chẩn đoán sơ bộ với độ tin cậy
        - 💊 Khuyến nghị điều trị phù hợp
        - ⚠️ Cảnh báo các dấu hiệu nguy hiểm cần đi khám ngay
        
        **Hãy mô tả các triệu chứng của bạn, tôi sẽ hỏi thêm nếu cần để hiểu rõ hơn!**
        
        _Ví dụ: "Tôi bị sốt cao, ho và đau đầu"_
        """
        st.markdown(f"""
        <div class="ai-message">
            {greeting}
        </div>
        """, unsafe_allow_html=True)
    
    # Display chat history
    for message in st.session_state.messages:
        role = message['role']
        content = message['content']
        
        if role == 'user':
            st.markdown(f"""
            <div class="user-message">
                <b>👤 Bạn:</b><br>{content}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="ai-message">
                <b>🏥 AI Doctor:</b><br>{content}
            </div>
            """, unsafe_allow_html=True)
    
    # Chat input
    user_input = st.chat_input("Nhập triệu chứng của bạn... (Ví dụ: Tôi bị sốt cao, ho và đau đầu)")
    
    if user_input:
        # Sanitize input
        user_input = sanitize_user_input(user_input)
        
        # Add user message
        SessionManager.add_message(st.session_state, 'user', user_input)
        
        # Get chat history
        chat_history = SessionManager.get_chat_history_text(st.session_state)
        
        # Show processing
        with st.spinner("🔍 Đang phân tích triệu chứng..."):
            try:
                # Analyze symptoms
                analysis_result = diagnosis_engine.analyze_symptoms(
                    user_input=user_input,
                    chat_history=chat_history,
                    accumulated_symptoms=st.session_state.user_symptoms
                )
                
                # Update accumulated symptoms
                st.session_state.user_symptoms = analysis_result['symptoms']
                
                # Generate diagnosis
                diagnosis_text = diagnosis_engine.generate_diagnosis(
                    user_input=user_input,
                    analysis_result=analysis_result,
                    chat_history=chat_history
                )
                
                # Add AI response
                SessionManager.add_message(st.session_state, 'assistant', diagnosis_text)
                
                logger.info("Successfully processed user input")
                
            except Exception as e:
                logger.error(f"Error processing user input: {e}")
                error_message = f"❌ Lỗi: {str(e)}\n\n💡 Vui lòng thử lại sau."
                SessionManager.add_message(st.session_state, 'assistant', error_message)
        
        # Rerun to show new messages
        st.rerun()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 1rem;">
        © 2025 AI Medical Diagnosis System | Powered by <b>Google Gemini AI</b><br>
        <a href="https://github.com/AnHgPham/ai-medical-diagnosis" target="_blank">GitHub</a> • 
        <a href="https://streamlit.io" target="_blank">Streamlit</a>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
