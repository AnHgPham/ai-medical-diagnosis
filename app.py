"""
AI Medical Diagnosis System - Streamlit App
Using Google Gemini API
Chat Interface Only
"""

import streamlit as st
import google.generativeai as genai
import json
import os

# Page configuration
st.set_page_config(
    page_title="AI Medical Diagnosis",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .chat-message {
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        flex-direction: column;
    }
    .user-message {
        background-color: #e3f2fd;
        border-left: 5px solid #2196F3;
    }
    .assistant-message {
        background-color: #f3e5f5;
        border-left: 5px solid #9c27b0;
    }
    .stTextInput > div > div > input {
        border-radius: 20px;
    }
    h1 {
        color: white;
        text-align: center;
    }
    .warning-box {
        background-color: #fff3cd;
        border-left: 5px solid #ffc107;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
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

# Initialize Gemini
def init_gemini():
    api_key = st.secrets.get("GEMINI_API_KEY", os.getenv("GEMINI_API_KEY"))
    if not api_key:
        st.error("⚠️ GEMINI_API_KEY not found. Please set it in Streamlit secrets or environment variables.")
        st.stop()
    
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-pro')

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
    st.session_state.chat_history = []

if 'knowledge_context' not in st.session_state:
    kb = load_knowledge_base()
    st.session_state.knowledge_context = build_knowledge_context(kb)

if 'model' not in st.session_state:
    st.session_state.model = init_gemini()

# Header
st.title("🤖 AI Medical Diagnosis System")
st.markdown("<p style='text-align: center; color: white; font-size: 1.2em;'>Powered by Google Gemini AI</p>", unsafe_allow_html=True)

# Warning box
st.markdown("""
<div class="warning-box">
    <strong>⚠️ Lưu ý quan trọng:</strong> Hệ thống này chỉ mang tính chất tham khảo và hỗ trợ học tập. 
    Không sử dụng để tự chẩn đoán và điều trị. Luôn tham khảo ý kiến bác sĩ chuyên khoa khi có vấn đề về sức khỏe.
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("ℹ️ Về Hệ Thống")
    st.markdown("""
    ### 🎯 Tính năng
    - 💬 Chat với AI Doctor
    - 🧠 Phân tích thông minh
    - 📊 Chẩn đoán chi tiết
    - 💊 Khuyến nghị điều trị
    
    ### 🔬 Công nghệ
    - **AI:** Google Gemini Pro
    - **Framework:** Streamlit
    - **Language:** Python 3.11
    
    ### 📋 Cơ sở tri thức
    - 5 bệnh phổ biến
    - 16 triệu chứng
    - Cập nhật liên tục
    """)
    
    if st.button("🔄 Bắt đầu cuộc trò chuyện mới"):
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
            <strong>👤 Bạn:</strong><br>
            {message["content"]}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="chat-message assistant-message">
            <strong>🤖 AI Doctor:</strong><br>
            {message["content"].replace('\n', '<br>')}
        </div>
        """, unsafe_allow_html=True)

# Initial greeting
if len(st.session_state.messages) == 0:
    greeting = """
    Xin chào! Tôi là AI Doctor, trợ lý y tế thông minh. 
    
    Tôi có thể giúp bạn:
    - 🩺 Phân tích các triệu chứng bạn đang gặp phải
    - 💡 Đưa ra chẩn đoán sơ bộ với độ tin cậy
    - 💊 Khuyến nghị hướng điều trị
    - ⚠️ Cảnh báo các dấu hiệu nguy hiểm
    
    Hãy mô tả các triệu chứng của bạn, tôi sẽ hỏi thêm nếu cần để hiểu rõ hơn!
    """
    st.markdown(f"""
    <div class="chat-message assistant-message">
        <strong>🤖 AI Doctor:</strong><br>
        {greeting.replace(chr(10), '<br>')}
    </div>
    """, unsafe_allow_html=True)

# Chat input
user_input = st.chat_input("Nhập triệu chứng của bạn...")

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
4. Explain your reasoning clearly
5. Give treatment recommendations
6. Warn about serious symptoms

Always respond in Vietnamese. Be empathetic and professional.
"""
    
    # Build conversation history
    conversation = []
    for msg in st.session_state.messages:
        conversation.append(f"{'Patient' if msg['role'] == 'user' else 'AI Doctor'}: {msg['content']}")
    
    full_prompt = f"{system_prompt}\n\nConversation:\n" + "\n".join(conversation) + "\n\nAI Doctor:"
    
    # Get response from Gemini
    try:
        with st.spinner("🤔 AI đang suy nghĩ..."):
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
<p style='text-align: center; color: white;'>
    © 2025 AI Medical Diagnosis System | Powered by Google Gemini | 
    <a href='https://github.com' style='color: white;'>GitHub</a>
</p>
""", unsafe_allow_html=True)
