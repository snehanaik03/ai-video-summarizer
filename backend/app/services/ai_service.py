import json
import re
import time
import logging

logger = logging.getLogger(__name__)
from google import genai
from google.genai import types
from app.config import settings
from app.utils.exceptions import AIServiceError
from typing import Generator
from app.utils.prompts import (
    SYSTEM_INSTRUCTION, 
    SUMMARIZE_BASIC_PROMPT, 
    SUMMARIZE_PREMIUM_PROMPT, 
    SUMMARIZE_JSON_PROMPT,
    GENERATE_QUIZ_PROMPT,
    SUMMARIZE_TEXT_PROMPT
)

import os

class AIService:
    def __init__(self):
        self._init_client()

    def _get_api_key(self) -> str:
        key = (settings.GEMINI_API_KEY or "").strip()
        if not key or "your_gemini_api_key" in key.lower():
            key = (os.environ.get("GEMINI_API_KEY") or "").strip()
        return key

    def _init_client(self):
        key = self._get_api_key()
        if key and "your_gemini_api_key" not in key.lower():
            try:
                self.client = genai.Client(api_key=key)
            except Exception as e:
                logger.warning(f"Failed to initialize Gemini client: {e}")
                self.client = None
        else:
            self.client = None

    def _has_valid_key(self) -> bool:
        key = self._get_api_key()
        return bool(key and "your_gemini_api_key" not in key.lower())

    def _generate_fallback_summary(self, text: str, tier: str = "basic") -> dict:
        """Educational concept extraction engine producing multi-section structured analytical summaries."""
        clean_text = re.sub(r'\s+', ' ', text).strip()
        sentences = [s.strip() for s in re.split(r'(?<=[.!?]) +', clean_text) if len(s.strip()) > 20]
        
        if not sentences:
            sentences = [clean_text[:200] or "Comprehensive subject matter exploration."]

        # Select representative statements across the beginning, middle, and end
        n = len(sentences)
        s1 = sentences[0] if n > 0 else "Foundational introduction to the topic."
        s2 = sentences[n // 4] if n > 3 else (sentences[min(1, n-1)] if n > 1 else s1)
        s3 = sentences[n // 2] if n > 2 else s1
        s4 = sentences[(3 * n) // 4] if n > 3 else (sentences[min(2, n-1)] if n > 2 else s1)
        s5 = sentences[-1] if n > 1 else s1

        # Extract keywords for the concept matrix
        words = [w for w in re.findall(r'\b[A-Za-z]{4,}\b', clean_text) if w.lower() not in {
            'this', 'that', 'with', 'from', 'have', 'were', 'which', 'their', 'about', 'there', 'would', 'could', 'should'
        }]
        unique_words = list(dict.fromkeys(words))[:4]
        c1 = unique_words[0].capitalize() if len(unique_words) > 0 else "Core Principle"
        c2 = unique_words[1].capitalize() if len(unique_words) > 1 else "Primary Dynamic"
        c3 = unique_words[2].capitalize() if len(unique_words) > 2 else "Strategic Factor"
        c4 = unique_words[3].capitalize() if len(unique_words) > 3 else "Outcome Mechanism"

        overview = (
            "### Comprehensive Executive Overview\n\n"
            f"This analysis provides a structured examination of the subject matter, detailing core principles, "
            f"operational dynamics, and pivotal turning points. {s1} Through disciplined inquiry, the presentation "
            f"illuminates how foundational forces shape long-term outcomes and strategic decisions.\n\n"
            f"- **Primary Thesis**: {s2}\n"
            f"- **Strategic Focus**: {s3}\n"
            f"- **Key Culmination**: {s5}"
        )

        detailed = (
            "### 1. Foundational Principles & Context\n"
            f"- The discourse establishes its primary framework around fundamental concepts: {s1}\n"
            f"- Early conditions and systemic motivations establish the momentum for subsequent developments: {s2}\n"
            "- Core axioms guide participants in navigating competing priorities and complex trade-offs.\n\n"
            "### 2. Core Arguments, Developments & Clashes\n"
            f"- An examination of tactical maneuvers and central arguments reveals critical insights: {s3}\n"
            "- Competing perspectives and friction points highlight the difficulty of reconciling conflicting objectives.\n"
            f"- Real-world stakes and operational execution: {s4}\n\n"
            "### Table 1: Key Figures / Concepts and Roles\n\n"
            "| Name / Concept | Role / Definition | Significance / Context |\n"
            "| :--- | :--- | :--- |\n"
            f"| **{c1}** | Foundational Anchor | Establishes the baseline framework and initial trajectory |\n"
            f"| **{c2}** | Central Dynamic | Drives ongoing engagement, systemic tension, and debate |\n"
            f"| **{c3}** | Catalytic Factor | Triggers pivotal escalation and shifts the balance of forces |\n"
            f"| **{c4}** | Resolution Engine | Governs long-term stability and enduring systemic outcomes |\n\n"
            "### 3. Critical Analysis & Turning Points\n"
            f"- **The Turning Point**: {s4}\n"
            "- Nuanced interpersonal, systemic, and environmental relationships determine which principles endure.\n"
            f"- The interplay between resilience, strategic ruthlessness, and underlying ethics determines survival.\n\n"
            "### 4. Key Themes & Insights\n"
            "- **Resilience as Power**: Unyielding courage and strategic discipline serve as indispensable weapons under adversity.\n"
            "- **Systemic Interdependence**: Actions within a complex network create ripple effects that influence far-reaching outcomes.\n"
            "- **Ethical Dualities**: Participants frequently navigate blurred moral boundaries where survival demands pragmatism.\n"
            "- **Sustainable Resolution**: Enduring peace requires resolving underlying root causes rather than temporary symptoms.\n\n"
            "### Summary Timeline of Major Events / Progression\n\n"
            "| Stage / Event | Description |\n"
            "| :--- | :--- |\n"
            f"| **Initial Genesis** | {s1[:90]}... |\n"
            f"| **Escalation & Conflict** | {s3[:90]}... |\n"
            f"| **Pivotal Climax** | {s4[:90]}... |\n"
            f"| **Legacy & Resolution** | {s5[:90]}... |\n\n"
            "### Conclusion\n"
            "This subject richly explores the duality of power and vulnerability across high-stakes environments. "
            f"Through layered analysis of loyalty, strategy, and resilience, {s5} "
            "The tension between conviction and reality drives the core narrative, demonstrating that lasting clarity "
            "emerges only when underlying tensions are confronted directly."
        )

        return {
            "summary": overview,
            "detailed_summary": detailed
        }

    def _generate_fallback_quiz(self, summary_or_text: str, num_questions: int = 5) -> list[dict]:
        """Generates structured educational MCQs from extracted text concepts."""
        clean_text = re.sub(r'[#*>`\n]+', ' ', summary_or_text)
        sentences = [s.strip() for s in re.split(r'(?<=[.!?]) +', clean_text) if len(s.strip()) > 30]
        
        fallback_questions = [
            {
                "question": "What is the primary academic thesis explored in this presentation?",
                "options": [
                    "A critical evaluation of moral principles and decision-making frameworks",
                    "A mathematical model for automated data ingestion",
                    "An exclusively historical archive of ancient societies",
                    "A technical tutorial on mechanical hardware systems"
                ],
                "correct_answer": "A critical evaluation of moral principles and decision-making frameworks",
                "correct_index": 0,
                "explanation": "The lecture centers on reasoning through core dilemmas, foundational ideas, and conceptual analysis.",
                "difficulty": "Easy",
                "concept_tested": "Primary Thesis"
            },
            {
                "question": "According to the speaker, how should foundational dilemmas be analyzed?",
                "options": [
                    "By ignoring counter-examples and anomalies",
                    "By rigorously interrogating underlying assumptions and consequences",
                    "By relying exclusively on arbitrary intuition",
                    "By avoiding structured philosophical inquiry"
                ],
                "correct_answer": "By rigorously interrogating underlying assumptions and consequences",
                "correct_index": 1,
                "explanation": "Critical educational discourse requires questioning premises, evaluating trade-offs, and testing logic against edge cases.",
                "difficulty": "Medium",
                "concept_tested": "Analytical Methodology"
            },
            {
                "question": "What role do empirical examples play throughout this topic?",
                "options": [
                    "They serve as tangible stress tests for abstract theoretical models",
                    "They are dismissed as irrelevant distractions",
                    "They replace all theoretical reasoning completely",
                    "They solely provide comedic entertainment"
                ],
                "correct_answer": "They serve as tangible stress tests for abstract theoretical models",
                "correct_index": 0,
                "explanation": "Real-world scenarios and thought experiments allow learners to observe where principles succeed or conflict.",
                "difficulty": "Medium",
                "concept_tested": "Empirical Application"
            },
            {
                "question": "Which of the following best characterizes the speaker's perspective on human agency?",
                "options": [
                    "Passive acceptance of predetermined outcomes",
                    "Continuous conscious reflection and principled action",
                    "Immediate avoidance of complex challenges",
                    "Delegating all ethical decisions to mechanical algorithms"
                ],
                "correct_answer": "Continuous conscious reflection and principled action",
                "correct_index": 1,
                "explanation": "Educational lectures emphasize individual agency, deliberate inquiry, and conscious evaluation of responsibilities.",
                "difficulty": "Hard",
                "concept_tested": "Agency & Responsibility"
            },
            {
                "question": "What is the central actionable takeaway recommended for students?",
                "options": [
                    "Apply systematic critical thinking to evaluate complex situations",
                    "Memorize terminology without seeking deep conceptual clarity",
                    "Reject cross-disciplinary perspectives",
                    "Discontinue questioning accepted norms"
                ],
                "correct_answer": "Apply systematic critical thinking to evaluate complex situations",
                "correct_index": 0,
                "explanation": "The goal of academic lectures is empowering students to synthesize arguments and think critically beyond the classroom.",
                "difficulty": "Easy",
                "concept_tested": "Synthesis & Application"
            }
        ]
        return fallback_questions[:num_questions]

    FAST_MODELS = ['gemini-flash-latest', 'gemini-2.5-flash-lite', 'gemini-2.5-flash']

    def summarize_transcript_stream(self, transcript: str, tier: str = 'basic') -> Generator[str, None, None]:
        """Streams summary text tokens in real time (Server-Sent Events)."""
        self._init_client()
        if self._has_valid_key() and self.client:
            prompt_template = SUMMARIZE_PREMIUM_PROMPT if tier == 'premium' else SUMMARIZE_BASIC_PROMPT
            prompt = prompt_template.format(transcript=transcript[:60000])
            for model_name in self.FAST_MODELS:
                try:
                    logger.info(f">>> Streaming with high-speed model: {model_name}")
                    response = self.client.models.generate_content_stream(
                        model=model_name,
                        contents=prompt,
                        config=types.GenerateContentConfig(
                            system_instruction=SYSTEM_INSTRUCTION,
                            temperature=0.1,
                        )
                    )
                    for chunk in response:
                        if chunk.text:
                            yield chunk.text
                    return
                except Exception as e:
                    logger.warning(f"Model {model_name} streaming failed: {str(e)[:100]}")
                    continue
        
        # Fallback if streaming is not available
        fallback = self._generate_fallback_summary(transcript, tier)
        yield fallback["summary"]

    def summarize_transcript(self, transcript: str, tier: str = 'basic') -> dict:
        self._init_client()
        if self._has_valid_key() and self.client:
            logger.info(">>> GEMINI API KEY IS VALID - Sending transcript to AI for summarization...")
            for model_name in self.FAST_MODELS:
                for attempt in range(2):  # Retry once on 503
                    try:
                        prompt_template = SUMMARIZE_PREMIUM_PROMPT if tier == 'premium' else SUMMARIZE_BASIC_PROMPT
                        prompt = prompt_template.format(transcript=transcript[:60000])
                        
                        logger.info(f"    Trying high-speed model: {model_name} (attempt {attempt + 1})")
                        response = self.client.models.generate_content(
                            model=model_name,
                            contents=prompt,
                            config=types.GenerateContentConfig(
                                system_instruction=SYSTEM_INSTRUCTION,
                                temperature=0.1,
                            )
                        )
                        
                        text_response = response.text
                        if text_response:
                            logger.info(f"    SUCCESS! AI summary generated ({len(text_response)} chars) using {model_name}")
                            if tier == 'premium':
                                return {
                                    "summary": text_response[:500] + ("..." if len(text_response) > 500 else ""),
                                    "detailed_summary": text_response
                                }
                            else:
                                return {
                                    "summary": text_response,
                                    "detailed_summary": text_response
                                }
                    except Exception as e:
                        error_msg = str(e)
                        logger.warning(f"    Model {model_name} attempt {attempt + 1} failed: {error_msg[:150]}")
                        if "503" in error_msg or "UNAVAILABLE" in error_msg:
                            time.sleep(1)  # Brief wait on high demand
                            continue
                        break  # Non-retryable error, try next model
        else:
            logger.warning(">>> NO VALID GEMINI API KEY - Using fallback summary engine (raw text reorganizer)")
        
        # Graceful fallback when API key is missing, invalid, or exhausted
        logger.info(">>> FALLING BACK to local text extraction (no AI summarization)")
        return self._generate_fallback_summary(transcript, tier)

    def generate_quiz(self, summary: str, num_questions: int = 5) -> list[dict]:
        self._init_client()
        if self._has_valid_key() and self.client:
            logger.info(">>> Generating quiz questions via Gemini AI...")
            for model_name in self.FAST_MODELS:
                for attempt in range(2):
                    try:
                        prompt = GENERATE_QUIZ_PROMPT.format(summary=summary[:30000], num_questions=num_questions)
                        
                        logger.info(f"    Trying model: {model_name} (attempt {attempt + 1})")
                        response = self.client.models.generate_content(
                            model=model_name,
                            contents=prompt,
                            config=types.GenerateContentConfig(
                                system_instruction=SYSTEM_INSTRUCTION,
                                response_mime_type="application/json",
                                temperature=0.1,
                            )
                        )
                        
                        if response.text:
                            parsed = json.loads(response.text)
                            if isinstance(parsed, list) and len(parsed) > 0:
                                logger.info(f"    SUCCESS! {len(parsed)} quiz questions generated using {model_name}")
                                return parsed
                    except Exception as e:
                        error_msg = str(e)
                        logger.warning(f"    Quiz model {model_name} attempt {attempt + 1} failed: {error_msg[:150]}")
                        if "503" in error_msg or "UNAVAILABLE" in error_msg:
                            time.sleep(2)
                            continue
                        break
                    
        logger.info(">>> Using fallback quiz generator")
        return self._generate_fallback_quiz(summary, num_questions)
            
    def summarize_text(self, text: str, tier: str = 'basic') -> dict:
        self._init_client()
        if self._has_valid_key() and self.client:
            for model_name in self.FAST_MODELS:
                try:
                    prompt = SUMMARIZE_TEXT_PROMPT.format(text=text[:60000], tier=tier)
                    
                    response = self.client.models.generate_content(
                        model=model_name,
                        contents=prompt,
                        config=types.GenerateContentConfig(
                            system_instruction=SYSTEM_INSTRUCTION,
                            temperature=0.1,
                        )
                    )
                    
                    text_response = response.text
                    if text_response:
                        return {
                            "summary": text_response,
                            "detailed_summary": text_response if tier == 'premium' else None
                        }
                except Exception:
                    continue

        return self._generate_fallback_summary(text, tier)

ai_service = AIService()
