"""
Knowledge Manager for AI Medical Diagnosis System
Handles loading, validation, and management of medical knowledge base
"""
import logging
from typing import List, Dict, Optional
from pathlib import Path

from config import KNOWLEDGE_BASE_PATH
from utils import (
    setup_logging, 
    load_json_file, 
    save_json_file,
    validate_symptoms_data,
    validate_diseases_data
)

logger = setup_logging(__name__)


class KnowledgeManager:
    """Manage medical knowledge base"""
    
    def __init__(self, knowledge_base_path: Path = KNOWLEDGE_BASE_PATH):
        """Initialize knowledge manager"""
        self.knowledge_base_path = knowledge_base_path
        self.knowledge_base = None
        self.diseases = []
        self.symptoms = []
        self.load_knowledge_base()
    
    def load_knowledge_base(self) -> Dict:
        """Load knowledge base from JSON file"""
        try:
            logger.info(f"Loading knowledge base from {self.knowledge_base_path}")
            self.knowledge_base = load_json_file(self.knowledge_base_path)
            
            # Extract diseases and symptoms
            self.diseases = self.knowledge_base.get('diseases', [])
            self.symptoms = self.knowledge_base.get('symptoms', [])
            
            # Validate data
            if not self.validate_knowledge_base():
                raise ValueError("Invalid knowledge base structure")
            
            logger.info(f"Loaded {len(self.diseases)} diseases and {len(self.symptoms)} symptoms")
            return self.knowledge_base
            
        except Exception as e:
            logger.error(f"Failed to load knowledge base: {e}")
            raise
    
    def validate_knowledge_base(self) -> bool:
        """Validate knowledge base structure"""
        try:
            if not validate_diseases_data(self.diseases):
                logger.error("Invalid diseases data structure")
                return False
            
            if not validate_symptoms_data(self.symptoms):
                logger.error("Invalid symptoms data structure")
                return False
            
            logger.info("Knowledge base validation passed")
            return True
            
        except Exception as e:
            logger.error(f"Validation error: {e}")
            return False
    
    def get_disease_by_id(self, disease_id: str) -> Optional[Dict]:
        """Get disease information by ID"""
        for disease in self.diseases:
            if disease['id'] == disease_id:
                return disease
        return None
    
    def get_disease_by_name(self, disease_name: str) -> Optional[Dict]:
        """Get disease information by name"""
        disease_name_lower = disease_name.lower()
        for disease in self.diseases:
            if disease['name'].lower() == disease_name_lower:
                return disease
        return None
    
    def get_symptom_by_id(self, symptom_id: str) -> Optional[Dict]:
        """Get symptom information by ID"""
        for symptom in self.symptoms:
            if symptom['id'] == symptom_id:
                return symptom
        return None
    
    def get_symptoms_by_category(self, category: str) -> List[Dict]:
        """Get all symptoms in a category"""
        return [s for s in self.symptoms if s.get('category') == category]
    
    def search_diseases_by_symptoms(self, symptom_ids: List[str]) -> List[Dict]:
        """Search diseases that match given symptoms"""
        matching_diseases = []
        
        for disease in self.diseases:
            disease_symptoms = set(disease.get('symptoms', []))
            user_symptoms = set(symptom_ids)
            
            # Check if any symptoms match
            if disease_symptoms & user_symptoms:
                match_count = len(disease_symptoms & user_symptoms)
                match_ratio = match_count / len(disease_symptoms) if disease_symptoms else 0
                
                matching_diseases.append({
                    'disease': disease,
                    'match_count': match_count,
                    'match_ratio': match_ratio,
                    'matched_symptoms': list(disease_symptoms & user_symptoms)
                })
        
        # Sort by match ratio descending
        matching_diseases.sort(key=lambda x: (x['match_ratio'], x['match_count']), reverse=True)
        
        return matching_diseases
    
    def get_all_diseases(self) -> List[Dict]:
        """Get all diseases"""
        return self.diseases
    
    def get_all_symptoms(self) -> List[Dict]:
        """Get all symptoms"""
        return self.symptoms
    
    def get_symptom_categories(self) -> List[str]:
        """Get unique symptom categories"""
        categories = set()
        for symptom in self.symptoms:
            if 'category' in symptom:
                categories.add(symptom['category'])
        return sorted(list(categories))
    
    def build_knowledge_context(self) -> str:
        """Build knowledge context string for LLM"""
        context_parts = []
        
        # Add diseases summary
        context_parts.append("=== CÁC BỆNH PHỔ BIẾN ===\n")
        for disease in self.diseases:
            context_parts.append(
                f"- {disease['name']} ({disease['id']}): "
                f"{disease.get('description', 'N/A')}"
            )
            context_parts.append(f"  Triệu chứng: {', '.join(disease.get('symptoms', []))}")
            if 'treatment' in disease:
                context_parts.append(f"  Điều trị: {disease['treatment']}")
            context_parts.append("")
        
        # Add symptoms summary
        context_parts.append("\n=== CÁC TRIỆU CHỨNG ===\n")
        
        # Group by category
        for category in self.get_symptom_categories():
            context_parts.append(f"\n{category}:")
            category_symptoms = self.get_symptoms_by_category(category)
            for symptom in category_symptoms:
                context_parts.append(f"  - {symptom['name']} ({symptom['id']})")
        
        return "\n".join(context_parts)
    
    def add_disease(self, disease_data: Dict) -> bool:
        """Add new disease to knowledge base"""
        try:
            # Validate required fields
            required_fields = ['id', 'name', 'symptoms']
            for field in required_fields:
                if field not in disease_data:
                    logger.error(f"Missing required field: {field}")
                    return False
            
            # Check if disease already exists
            if self.get_disease_by_id(disease_data['id']):
                logger.error(f"Disease {disease_data['id']} already exists")
                return False
            
            # Add disease
            self.diseases.append(disease_data)
            self.knowledge_base['diseases'] = self.diseases
            
            # Save to file
            save_json_file(self.knowledge_base, self.knowledge_base_path)
            
            logger.info(f"Added disease: {disease_data['name']}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to add disease: {e}")
            return False
    
    def add_symptom(self, symptom_data: Dict) -> bool:
        """Add new symptom to knowledge base"""
        try:
            # Validate required fields
            required_fields = ['id', 'name', 'category']
            for field in required_fields:
                if field not in symptom_data:
                    logger.error(f"Missing required field: {field}")
                    return False
            
            # Check if symptom already exists
            if self.get_symptom_by_id(symptom_data['id']):
                logger.error(f"Symptom {symptom_data['id']} already exists")
                return False
            
            # Add symptom
            self.symptoms.append(symptom_data)
            self.knowledge_base['symptoms'] = self.symptoms
            
            # Save to file
            save_json_file(self.knowledge_base, self.knowledge_base_path)
            
            logger.info(f"Added symptom: {symptom_data['name']}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to add symptom: {e}")
            return False
    
    def get_statistics(self) -> Dict:
        """Get knowledge base statistics"""
        return {
            'total_diseases': len(self.diseases),
            'total_symptoms': len(self.symptoms),
            'symptom_categories': len(self.get_symptom_categories()),
            'avg_symptoms_per_disease': sum(len(d.get('symptoms', [])) for d in self.diseases) / len(self.diseases) if self.diseases else 0
        }


# Export
__all__ = ['KnowledgeManager']
