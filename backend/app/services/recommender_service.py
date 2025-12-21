"""
RAG-based recommender service - follows SOLID principles
Single Responsibility: Handles AI-powered food recommendations
"""
from typing import List, Dict, Optional
from sqlalchemy.orm import Session
try:
    from langchain.embeddings import OpenAIEmbeddings
    from langchain.vectorstores import FAISS
    from langchain.llms import OpenAI
    from langchain.chains import RetrievalQA
    from langchain.prompts import PromptTemplate
    LANGCHAIN_AVAILABLE = True
except ImportError:
    LANGCHAIN_AVAILABLE = False
from app.core.config import settings
from app.models.food import Food
from app.models.preference import UserPreference
from app.services.food_service import FoodService
import json


class RecommenderService:
    """
    RAG-based recommender for healthier menu suggestions
    Uses Retrieval-Augmented Generation for context-aware recommendations
    """
    
    def __init__(self):
        """Initialize the recommender with OpenAI"""
        if settings.OPENAI_API_KEY and LANGCHAIN_AVAILABLE:
            try:
                self.embeddings = OpenAIEmbeddings(openai_api_key=settings.OPENAI_API_KEY)
                self.llm = OpenAI(temperature=0.7, openai_api_key=settings.OPENAI_API_KEY)
                self.vector_store = None
                self.qa_chain = None
            except Exception:
                self.embeddings = None
                self.llm = None
                self.vector_store = None
                self.qa_chain = None
        else:
            self.embeddings = None
            self.llm = None
            self.vector_store = None
            self.qa_chain = None
    
    def _build_food_knowledge_base(self, db: Session) -> None:
        """Build vector store from food database"""
        if not self.embeddings:
            return
        
        foods = FoodService.get_all_foods(db, limit=1000)
        
        # Create documents from food data
        documents = []
        for food in foods:
            doc_text = f"""
            Food: {food.name}
            Description: {food.description or 'N/A'}
            Calories per 100g: {food.calories_per_100g}
            Protein per 100g: {food.protein_per_100g}g
            Carbs per 100g: {food.carbs_per_100g}g
            Fats per 100g: {food.fats_per_100g}g
            Fiber per 100g: {food.fiber_per_100g}g
            """
            documents.append(doc_text)
        
        if documents:
            self.vector_store = FAISS.from_texts(documents, self.embeddings)
            
            # Create QA chain
            prompt_template = PromptTemplate(
                input_variables=["context", "question"],
                template="""
                You are a nutrition expert. Based on the following food database and user preferences,
                provide healthy food recommendations.
                
                Context: {context}
                
                Question: {question}
                
                Provide specific food recommendations with reasoning.
                """
            )
            
            self.qa_chain = RetrievalQA.from_chain_type(
                llm=self.llm,
                chain_type="stuff",
                retriever=self.vector_store.as_retriever(search_kwargs={"k": 5}),
                chain_type_kwargs={"prompt": prompt_template}
            )
    
    def get_recommendations(
        self,
        db: Session,
        user_id: int,
        target_calories: Optional[float] = None,
        dietary_restrictions: Optional[List[str]] = None
    ) -> List[Dict]:
        """
        Get personalized food recommendations using RAG
        """
        if not self.llm or not self.vector_store:
            # Fallback to rule-based recommendations if AI is not available
            return self._get_fallback_recommendations(db, target_calories, dietary_restrictions)
        
        # Build knowledge base if not already built
        if not self.vector_store:
            self._build_food_knowledge_base(db)
        
        # Get user preferences
        from app.services.preference_service import PreferenceService
        preferences = PreferenceService.get_user_preferences(db, user_id)
        
        # Build query
        query = f"""
        I need food recommendations for a user with:
        - Target calories: {target_calories or preferences.target_calories if preferences else 'flexible'}
        - Dietary restrictions: {', '.join(dietary_restrictions) if dietary_restrictions else 'none'}
        
        Suggest 5-7 healthy food options that fit these criteria.
        """
        
        # Get recommendations from RAG
        result = self.qa_chain.run(query)
        
        # Parse and return recommendations
        # In a real implementation, you'd parse the LLM response and match to actual foods
        return self._parse_recommendations(db, result, target_calories, dietary_restrictions)
    
    def _get_fallback_recommendations(
        self,
        db: Session,
        target_calories: Optional[float],
        dietary_restrictions: Optional[List[str]]
    ) -> List[Dict]:
        """Fallback rule-based recommendations"""
        query = db.query(Food)
        
        # Apply filters based on dietary restrictions
        if dietary_restrictions:
            if "vegetarian" in dietary_restrictions:
                query = query.filter(~Food.name.like("%chicken%"))
                query = query.filter(~Food.name.like("%beef%"))
                query = query.filter(~Food.name.like("%pork%"))
            if "vegan" in dietary_restrictions:
                query = query.filter(~Food.name.like("%egg%"))
                query = query.filter(~Food.name.like("%yogurt%"))
                query = query.filter(~Food.name.like("%milk%"))
        
        # Get high-protein, moderate-calorie foods
        foods = query.filter(
            Food.protein_per_100g >= 10,
            Food.calories_per_100g <= 200
        ).limit(7).all()
        
        return [
            {
                "id": food.id,
                "name": food.name,
                "calories_per_100g": food.calories_per_100g,
                "protein_per_100g": food.protein_per_100g,
                "reason": "High protein, moderate calories"
            }
            for food in foods
        ]
    
    def _parse_recommendations(
        self,
        db: Session,
        llm_response: str,
        target_calories: Optional[float],
        dietary_restrictions: Optional[List[str]]
    ) -> List[Dict]:
        """Parse LLM response and match to actual foods"""
        # In a production system, you'd use more sophisticated parsing
        # For now, use fallback
        return self._get_fallback_recommendations(db, target_calories, dietary_restrictions)

