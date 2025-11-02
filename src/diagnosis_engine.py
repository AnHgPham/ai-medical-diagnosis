"""
Diagnosis Engine for AI Medical Diagnosis System
Core logic for analyzing symptoms and generating diagnosis
"""
import logging
from typing import List, Dict, Tuple, Optional

from config import TOP_K_DISEASES, CONFIDENCE_THRESHOLD, MIN_SYMPTOMS_FOR_DIAGNOSIS
from knowledge_manager import KnowledgeManager
from medical_llm_handler import MedicalLLMHandler
from utils import (
    setup_logging,
    extract_symptoms_from_text,
    rank_diseases_by_symptoms,
    format_disease_info
)

logger = setup_logging(__name__)


class DiagnosisEngine:
    """Core diagnosis engine"""
    
    def __init__(self,
                 knowledge_manager: KnowledgeManager,
                 llm_handler: MedicalLLMHandler):
        """Initialize diagnosis engine"""
        self.knowledge_manager = knowledge_manager
        self.llm_handler = llm_handler
        logger.info("Diagnosis engine initialized")
    
    def extract_symptoms_from_input(self, user_input: str) -> List[str]:
        """Extract symptoms from user input"""
        try:
            # Get all known symptom names
            all_symptoms = [s['name'] for s in self.knowledge_manager.get_all_symptoms()]
            
            # Extract mentioned symptoms
            found_symptoms = extract_symptoms_from_text(user_input, all_symptoms)
            
            logger.info(f"Extracted {len(found_symptoms)} symptoms from input")
            return found_symptoms
            
        except Exception as e:
            logger.error(f"Error extracting symptoms: {e}")
            return []
    
    def match_diseases(self, symptoms: List[str], top_k: int = TOP_K_DISEASES) -> List[Dict]:
        """Match diseases based on symptoms"""
        try:
            if not symptoms:
                logger.warning("No symptoms provided for matching")
                return []
            
            # Get all diseases
            diseases = self.knowledge_manager.get_all_diseases()
            
            # Rank diseases by symptom matching
            ranked_diseases = rank_diseases_by_symptoms(symptoms, diseases, top_k)
            
            logger.info(f"Matched {len(ranked_diseases)} diseases")
            return ranked_diseases
            
        except Exception as e:
            logger.error(f"Error matching diseases: {e}")
            return []
    
    def calculate_confidence(self, matched_disease: Dict) -> float:
        """Calculate confidence score for a diagnosis"""
        try:
            score = matched_disease.get('score', 0.0)
            match_count = matched_disease.get('match_count', 0)
            
            # Adjust confidence based on number of matched symptoms
            if match_count >= 5:
                confidence = min(score * 1.2, 1.0)
            elif match_count >= 3:
                confidence = score
            else:
                confidence = score * 0.8
            
            return confidence
            
        except Exception as e:
            logger.error(f"Error calculating confidence: {e}")
            return 0.0
    
    def analyze_symptoms(self, 
                        user_input: str,
                        chat_history: str = "",
                        accumulated_symptoms: List[str] = None) -> Dict:
        """Analyze symptoms and provide diagnosis"""
        try:
            logger.info("Starting symptom analysis")
            
            # Extract symptoms from current input
            new_symptoms = self.extract_symptoms_from_input(user_input)
            
            # Combine with accumulated symptoms
            if accumulated_symptoms:
                all_symptoms = list(set(accumulated_symptoms + new_symptoms))
            else:
                all_symptoms = new_symptoms
            
            logger.info(f"Total symptoms: {len(all_symptoms)}")
            
            # Check for emergency symptoms
            emergency_warning = self.llm_handler.check_emergency_symptoms(all_symptoms)
            
            # Match diseases
            matched_diseases = self.match_diseases(all_symptoms)
            
            # Calculate confidence for top disease
            top_confidence = 0.0
            if matched_diseases:
                top_confidence = self.calculate_confidence(matched_diseases[0])
            
            # Determine if we have enough information
            has_enough_info = (
                len(all_symptoms) >= MIN_SYMPTOMS_FOR_DIAGNOSIS and
                matched_diseases and
                top_confidence >= CONFIDENCE_THRESHOLD
            )
            
            return {
                'symptoms': all_symptoms,
                'new_symptoms': new_symptoms,
                'matched_diseases': matched_diseases,
                'top_confidence': top_confidence,
                'has_enough_info': has_enough_info,
                'emergency_warning': emergency_warning
            }
            
        except Exception as e:
            logger.error(f"Error analyzing symptoms: {e}")
            return {
                'symptoms': [],
                'new_symptoms': [],
                'matched_diseases': [],
                'top_confidence': 0.0,
                'has_enough_info': False,
                'emergency_warning': None
            }
    
    def generate_diagnosis(self,
                          user_input: str,
                          analysis_result: Dict,
                          chat_history: str = "") -> str:
        """Generate diagnosis using LLM"""
        try:
            logger.info("Generating diagnosis")
            
            # Build symptoms info
            symptoms = analysis_result.get('symptoms', [])
            symptoms_info = "**Triệu chứng đã xác định:**\n"
            if symptoms:
                symptoms_info += "\n".join([f"- {s}" for s in symptoms])
            else:
                symptoms_info += "Chưa xác định được triệu chứng cụ thể"
            
            # Add matched diseases info
            matched_diseases = analysis_result.get('matched_diseases', [])
            if matched_diseases:
                symptoms_info += "\n\n**Các bệnh có khả năng cao:**\n"
                for i, disease_info in enumerate(matched_diseases[:3], 1):
                    disease = disease_info['disease']
                    score = disease_info.get('score', 0)
                    confidence = self.calculate_confidence(disease_info)
                    symptoms_info += f"{i}. {disease['name']} (Độ khớp: {score*100:.0f}%, Độ tin cậy: {confidence*100:.0f}%)\n"
                    symptoms_info += f"   - Mô tả: {disease.get('description', 'N/A')}\n"
            
            # Get knowledge context
            knowledge_context = self.knowledge_manager.build_knowledge_context()
            
            # Check for emergency
            emergency_warning = analysis_result.get('emergency_warning')
            if emergency_warning:
                return emergency_warning
            
            # Generate diagnosis response
            diagnosis_text = self.llm_handler.generate_diagnosis(
                user_input=user_input,
                knowledge_context=knowledge_context,
                chat_history=chat_history,
                symptoms_info=symptoms_info
            )
            
            # Format response
            formatted_response = self.llm_handler.format_medical_response(
                diagnosis_text=diagnosis_text,
                confidence=analysis_result.get('top_confidence'),
                matched_diseases=matched_diseases
            )
            
            logger.info("Successfully generated diagnosis")
            return formatted_response
            
        except Exception as e:
            logger.error(f"Error generating diagnosis: {e}")
            return f"❌ Lỗi khi tạo chẩn đoán: {str(e)}"
    
    def generate_follow_up_questions(self, analysis_result: Dict) -> Optional[str]:
        """Generate follow-up questions if needed"""
        try:
            symptoms = analysis_result.get('symptoms', [])
            matched_diseases = analysis_result.get('matched_diseases', [])
            has_enough_info = analysis_result.get('has_enough_info', False)
            
            # Only generate follow-up if we don't have enough info
            if has_enough_info or not matched_diseases:
                return None
            
            # Get top diseases
            top_diseases = [d['disease'] for d in matched_diseases[:3]]
            
            # Generate questions
            questions = self.llm_handler.generate_follow_up_questions(
                current_symptoms=symptoms,
                possible_diseases=top_diseases
            )
            
            return questions if questions else None
            
        except Exception as e:
            logger.error(f"Error generating follow-up questions: {e}")
            return None
    
    def assess_severity(self, symptoms: List[str]) -> Dict:
        """Assess severity of condition"""
        try:
            return self.llm_handler.assess_severity(symptoms)
        except Exception as e:
            logger.error(f"Error assessing severity: {e}")
            return {
                "severity_level": "unknown",
                "urgency": "should_see_doctor_soon",
                "explanation": str(e)
            }
    
    def get_treatment_recommendations(self,
                                     diagnosis: str,
                                     symptoms: List[str]) -> str:
        """Get treatment recommendations"""
        try:
            return self.llm_handler.generate_treatment_recommendations(
                diagnosis=diagnosis,
                symptoms=symptoms
            )
        except Exception as e:
            logger.error(f"Error getting treatment recommendations: {e}")
            return ""
    
    def generate_diagnosis_report(self, 
                                 user_input: str,
                                 analysis_result: Dict,
                                 diagnosis_text: str) -> Dict:
        """Generate comprehensive diagnosis report"""
        try:
            symptoms = analysis_result.get('symptoms', [])
            matched_diseases = analysis_result.get('matched_diseases', [])
            
            # Assess severity
            severity = self.assess_severity(symptoms)
            
            # Get top diagnosis
            top_diagnosis = matched_diseases[0]['disease']['name'] if matched_diseases else "Chưa xác định"
            
            # Get treatment recommendations
            treatment = self.get_treatment_recommendations(top_diagnosis, symptoms)
            
            report = {
                'timestamp': None,  # Will be set by caller
                'symptoms': symptoms,
                'matched_diseases': [d['disease']['name'] for d in matched_diseases[:3]],
                'top_diagnosis': top_diagnosis,
                'confidence': analysis_result.get('top_confidence', 0.0),
                'severity': severity,
                'diagnosis_text': diagnosis_text,
                'treatment_recommendations': treatment,
                'emergency_warning': analysis_result.get('emergency_warning')
            }
            
            logger.info("Generated diagnosis report")
            return report
            
        except Exception as e:
            logger.error(f"Error generating diagnosis report: {e}")
            return {}


# Export
__all__ = ['DiagnosisEngine']
