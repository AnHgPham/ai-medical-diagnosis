"""
AI Medical Diagnosis System - Streamlit App
Using Google Gemini API
Modern & Clean UI Design
"""

import streamlit as st
import google.generativeai as genai
import json
import os

# Page configuration
st.set_page_config(
    page_title="AI Medical Diagnosis",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Modern Custom CSS
st.markdown("""
<style>
    /* Main background */
    .main {
        background: linear-gradient(to bottom, #f8f9fa 0%, #e9ecef 100%);
    }
    
    .stApp {
        background: linear-gradient(to bottom, #f8f9fa 0%, #e9ecef 100%);
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .main-header h1 {
        color: white;
        text-align: center;
        margin: 0;
        font-size: 2.5rem;
        font-weight: 700;
    }
    
    .main-header p {
        color: rgba(255, 255, 255, 0.9);
        text-align: center;
        margin: 0.5rem 0 0 0;
        font-size: 1.1rem;
    }
    
    /* Chat message styling */
    .chat-message {
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 1.5rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        animation: fadeIn 0.3s ease-in;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        margin-left: 20%;
    }
    
    .user-message strong {
        color: #fff;
        font-size: 1.1rem;
    }
    
    .assistant-message {
        background: white;
        color: #333;
        margin-right: 20%;
        border: 1px solid #e0e0e0;
    }
    
    .assistant-message strong {
        color: #667eea;
        font-size: 1.1rem;
    }
    
    /* Warning box */
    .warning-box {
        background: linear-gradient(135deg, #fff3cd 0%, #ffe69c 100%);
        border-left: 5px solid #ffc107;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1.5rem 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    .warning-box strong {
        color: #856404;
    }
    
    /* Sidebar styling */
    .sidebar .sidebar-content {
        background: white;
        border-radius: 10px;
        padding: 1rem;
    }
    
    /* Info card */
    .info-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    .info-card h3 {
        color: #667eea;
        margin-top: 0;
    }
    
    /* Stats card */
    .stats-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .stats-card h2 {
        margin: 0;
        font-size: 2.5rem;
    }
    
    .stats-card p {
        margin: 0.5rem 0 0 0;
        opacity: 0.9;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(102, 126, 234, 0.4);
    }
    
    /* Chat input */
    .stChatInput {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        padding: 1rem 2rem;
        background: white;
        box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.1);
        z-index: 1000;
    }
    
    .stChatInput > div {
        border-radius: 30px;
        border: 2px solid #667eea;
        box-shadow: 0 2px 8px rgba(102, 126, 234, 0.2);
    }
    
    .stChatInput input {
        font-size: 1rem;
        padding: 1rem;
    }
    
    .stChatInput input::placeholder {
        color: #999;
        font-style: italic;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem;
        color: #666;
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

# Load knowledge base
@st.cache_data
def load_knowledge_base():
    with open('knowledge_base.json', 'r', encoding='utf-8') as f:
        return json.load(f)

# Build knowledge context for Gemini
@st.cache_data
def build_knowledge_context(kb):
    context_parts = []
    
    context_parts.append("# MEDICAL KNOWLEDGE BASE\n")
    context_parts.append("You are an expert medical diagnosis assistant. Use the following knowledge to help diagnose patients.\n")
    
    # Add disease information
    context_parts.append("\n## DISEASES:\n")
    for disease in kb['diseases']:
        context_parts.append(f"\n### {disease['name']} (ID: {disease['id']})")
        context_parts.append(f"- Description: {disease['description']}")
        context_parts.append(f"- Severity: {disease['severity']}")
        context_parts.append(f"- Common symptoms: {', '.join(disease['symptoms'])}")
        context_parts.append(f"- Treatment: {disease['treatment']}")
    
    # Add symptom information
    context_parts.append("\n\n## SYMPTOMS:\n")
    for symptom in kb['symptoms']:
        context_parts.append(f"- {symptom['id']}: {symptom['name']} (Category: {symptom['category']})")
    
    return "\n".join(context_parts)

# Initialize Gemini with updated model
def init_gemini():
    api_key = st.secrets.get("GEMINI_API_KEY", os.getenv("GEMINI_API_KEY"))
    if not api_key:
        st.error("⚠️ GEMINI_API_KEY not found. Please set it in Streamlit secrets or environment variables.")
        st.stop()
    
    genai.configure(api_key=api_key)
    # Use gemini-1.5-flash instead of deprecated gemini-pro
    return genai.GenerativeModel('gemini-1.5-flash')

# Initialize session state - Load knowledge base first
if 'kb' not in st.session_state:
    st.session_state.kb = load_knowledge_base()

if 'knowledge_context' not in st.session_state:
    st.session_state.knowledge_context = build_knowledge_context(st.session_state.kb)

if 'model' not in st.session_state:
    st.session_state.model = init_gemini()

if 'messages' not in st.session_state:
    st.session_state.messages = []
    st.session_state.chat_history = []

# Header
st.markdown("""
<div class="main-header">
    <h1>🏥 AI Medical Diagnosis System</h1>
    <p>Hệ thống chẩn đoán y tế thông minh | Powered by Google Gemini AI</p>
</div>
""", unsafe_allow_html=True)

# Warning box
st.markdown("""
<div class="warning-box">
    <strong>⚠️ Lưu ý quan trọng:</strong> Hệ thống này chỉ mang tính chất tham khảo và hỗ trợ học tập. 
    Không sử dụng để tự chẩn đoán và điều trị. Luôn tham khảo ý kiến bác sĩ chuyên khoa khi có vấn đề về sức khỏe.
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### 📊 Thống kê hệ thống")
    
    # Stats cards - kb is guaranteed to be loaded
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class="stats-card">
            <h2>{len(st.session_state.kb['diseases'])}</h2>
            <p>Bệnh phổ biến</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="stats-card">
            <h2>{len(st.session_state.kb['symptoms'])}</h2>
            <p>Triệu chứng</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Info card
    st.markdown("""
    <div class="info-card">
        <h3>🎯 Tính năng</h3>
        <ul>
            <li>💬 Chat với AI Doctor</li>
            <li>🧠 Phân tích thông minh</li>
            <li>📊 Chẩn đoán chi tiết</li>
            <li>💊 Khuyến nghị điều trị</li>
            <li>⚠️ Cảnh báo nguy hiểm</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-card">
        <h3>🔬 Công nghệ</h3>
        <ul>
            <li><strong>AI Model:</strong> Google Gemini 1.5 Flash</li>
            <li><strong>Framework:</strong> Streamlit</li>
            <li><strong>Language:</strong> Python 3.11</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    if st.button("🔄 Bắt đầu cuộc trò chuyện mới", use_container_width=True):
        st.session_state.messages = []
        st.session_state.chat_history = []
        st.rerun()

# Main chat interface
st.markdown("---")

# Display chat messages
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f"""
        <div class="chat-message user-message">
            <strong>👤 Bạn</strong><br><br>
            {message["content"]}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="chat-message assistant-message">
            <strong>🤖 AI Doctor</strong><br><br>
            {message["content"].replace('\n', '<br>')}
        </div>
        """, unsafe_allow_html=True)

# Initial greeting
if len(st.session_state.messages) == 0:
    greeting = """
    Xin chào! Tôi là AI Doctor, trợ lý y tế thông minh được hỗ trợ bởi Google Gemini AI. 
    
    <strong>Tôi có thể giúp bạn:</strong>
    <ul>
        <li>🩺 Phân tích các triệu chứng bạn đang gặp phải</li>
        <li>💡 Đưa ra chẩn đoán sơ bộ với độ tin cậy</li>
        <li>💊 Khuyến nghị hướng điều trị phù hợp</li>
        <li>⚠️ Cảnh báo các dấu hiệu nguy hiểm cần đi khám ngay</li>
    </ul>
    
    <strong>Hãy mô tả các triệu chứng của bạn, tôi sẽ hỏi thêm nếu cần để hiểu rõ hơn!</strong>
    """
    st.markdown(f"""
    <div class="chat-message assistant-message">
        <strong>🤖 AI Doctor</strong><br><br>
        {greeting}
    </div>
    """, unsafe_allow_html=True)

# Chat input with improved UI
st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)
user_input = st.chat_input("💬 Nhập triệu chứng của bạn... (Ví dụ: Tôi bị sốt cao, ho và đau đầu)")

if user_input:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Prepare prompt for Gemini
    system_prompt = f"""
{st.session_state.knowledge_context}

You are a friendly and professional medical AI assistant. Your role is to:
1. Listen carefully to the patient's symptoms
2. Ask clarifying questions when needed
3. Provide diagnosis with confidence levels
4. Explain your reasoning clearly in Vietnamese
5. Give treatment recommendations
6. Warn about serious symptoms that need immediate medical attention

Always respond in Vietnamese. Be empathetic, professional, and thorough.
Format your responses clearly with proper structure.
"""
    
    # Build conversation history
    conversation = []
    for msg in st.session_state.messages:
        conversation.append(f"{'Patient' if msg['role'] == 'user' else 'AI Doctor'}: {msg['content']}")
    
    full_prompt = f"{system_prompt}\n\nConversation:\n" + "\n".join(conversation) + "\n\nAI Doctor:"
    
    # Get response from Gemini
    try:
        with st.spinner("🤔 AI đang phân tích triệu chứng..."):
            response = st.session_state.model.generate_content(
                full_prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.7,
                    max_output_tokens=2000,
                )
            )
            
            ai_response = response.text
            
            # Add assistant message
            st.session_state.messages.append({"role": "assistant", "content": ai_response})
            
            # Rerun to display new messages
            st.rerun()
            
    except Exception as e:
        st.error(f"❌ Lỗi: {str(e)}")
        st.info("💡 Vui lòng kiểm tra API key hoặc thử lại sau.")

# Footer
st.markdown("---")
st.markdown("""
<div class="footer">
    <p>© 2025 AI Medical Diagnosis System | Powered by <strong>Google Gemini AI</strong></p>
    <p>
        <a href="https://github.com/AnHgPham/ai-medical-diagnosis" target="_blank">GitHub</a> • 
        <a href="https://streamlit.io" target="_blank">Streamlit</a>
    </p>
</div>
""", unsafe_allow_html=True)
