"""
Utility functions for AI Medical Diagnosis System
"""
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any
import json

from config import LOG_FORMAT, LOG_LEVEL, LOG_FILE


def setup_logging(name: str = __name__) -> logging.Logger:
    """Setup logging configuration"""
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, LOG_LEVEL))
    
    # File handler
    fh = logging.FileHandler(LOG_FILE)
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(logging.Formatter(LOG_FORMAT))
    
    # Console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(logging.Formatter(LOG_FORMAT))
    
    logger.addHandler(fh)
    logger.addHandler(ch)
    
    return logger


def load_json_file(file_path: Path) -> Dict:
    """Load JSON file safely"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in {file_path}: {e}")


def save_json_file(data: Dict, file_path: Path) -> None:
    """Save data to JSON file"""
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        raise IOError(f"Failed to save JSON to {file_path}: {e}")


def format_timestamp(dt: datetime = None) -> str:
    """Format datetime to string"""
    if dt is None:
        dt = datetime.now()
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def extract_symptoms_from_text(text: str, known_symptoms: List[str]) -> List[str]:
    """Extract symptoms mentioned in text"""
    text_lower = text.lower()
    found_symptoms = []
    
    for symptom in known_symptoms:
        symptom_lower = symptom.lower()
        if symptom_lower in text_lower:
            found_symptoms.append(symptom)
    
    return found_symptoms


def calculate_symptom_match_score(user_symptoms: List[str], 
                                  disease_symptoms: List[str]) -> float:
    """Calculate match score between user symptoms and disease symptoms"""
    if not user_symptoms or not disease_symptoms:
        return 0.0
    
    user_set = set(s.lower() for s in user_symptoms)
    disease_set = set(s.lower() for s in disease_symptoms)
    
    # Jaccard similarity
    intersection = len(user_set & disease_set)
    union = len(user_set | disease_set)
    
    return intersection / union if union > 0 else 0.0


def rank_diseases_by_symptoms(user_symptoms: List[str], 
                              diseases: List[Dict],
                              top_k: int = 5) -> List[Dict]:
    """Rank diseases by symptom matching score"""
    scored_diseases = []
    
    for disease in diseases:
        disease_symptoms = disease.get('symptoms', [])
        score = calculate_symptom_match_score(user_symptoms, disease_symptoms)
        
        if score > 0:
            scored_diseases.append({
                'disease': disease,
                'score': score,
                'matched_symptoms': list(set(user_symptoms) & set(disease_symptoms))
            })
    
    # Sort by score descending
    scored_diseases.sort(key=lambda x: x['score'], reverse=True)
    
    return scored_diseases[:top_k]


def format_disease_info(disease: Dict) -> str:
    """Format disease information for display"""
    info = f"**{disease['name']}** ({disease['id']})\n"
    info += f"- **Mô tả:** {disease.get('description', 'N/A')}\n"
    info += f"- **Triệu chứng:** {', '.join(disease.get('symptoms', []))}\n"
    info += f"- **Điều trị:** {disease.get('treatment', 'N/A')}\n"
    info += f"- **Mức độ:** {disease.get('severity', 'N/A')}\n"
    return info


def sanitize_user_input(text: str) -> str:
    """Sanitize user input"""
    # Remove excessive whitespace
    text = ' '.join(text.split())
    # Remove potentially harmful characters
    text = text.replace('<', '').replace('>', '')
    return text.strip()


def validate_symptoms_data(symptoms: List[Dict]) -> bool:
    """Validate symptoms data structure"""
    required_fields = ['id', 'name', 'category']
    
    for symptom in symptoms:
        for field in required_fields:
            if field not in symptom:
                return False
    
    return True


def validate_diseases_data(diseases: List[Dict]) -> bool:
    """Validate diseases data structure"""
    required_fields = ['id', 'name', 'symptoms']
    
    for disease in diseases:
        for field in required_fields:
            if field not in disease:
                return False
        
        if not isinstance(disease['symptoms'], list):
            return False
    
    return True


class SessionManager:
    """Manage user session data"""
    
    @staticmethod
    def initialize_session(session_state) -> None:
        """Initialize session state variables"""
        if 'messages' not in session_state:
            session_state.messages = []
        
        if 'chat_history' not in session_state:
            session_state.chat_history = []
        
        if 'user_symptoms' not in session_state:
            session_state.user_symptoms = []
        
        if 'diagnosis_history' not in session_state:
            session_state.diagnosis_history = []
    
    @staticmethod
    def add_message(session_state, role: str, content: str) -> None:
        """Add message to session"""
        session_state.messages.append({
            'role': role,
            'content': content,
            'timestamp': format_timestamp()
        })
    
    @staticmethod
    def get_chat_history_text(session_state, max_messages: int = 10) -> str:
        """Get formatted chat history"""
        messages = session_state.messages[-max_messages:]
        history = []
        
        for msg in messages:
            role = "User" if msg['role'] == 'user' else "AI Doctor"
            history.append(f"{role}: {msg['content']}")
        
        return "\n".join(history)


# Export commonly used functions
__all__ = [
    'setup_logging',
    'load_json_file',
    'save_json_file',
    'format_timestamp',
    'extract_symptoms_from_text',
    'calculate_symptom_match_score',
    'rank_diseases_by_symptoms',
    'format_disease_info',
    'sanitize_user_input',
    'validate_symptoms_data',
    'validate_diseases_data',
    'SessionManager'
]
