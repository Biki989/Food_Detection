from pydantic import BaseModel
from typing import List, Optional

class NutritionInfo(BaseModel):
    calories: float
    protein: float
    carbohydrates: float
    fats: float
    fiber: float
    sugar: float
    sodium: float
    ingredients: List[str]

class AllergyInfo(BaseModel):
    allergens_detected: List[str]
    warnings: List[str]

class AnalyzeResponse(BaseModel):
    food_name: str
    confidence: float
    top_predictions: List[str]
    nutrition: NutritionInfo
    allergy_info: AllergyInfo
    dietary_classification: str
    health_recommendation: List[str]
