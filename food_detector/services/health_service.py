from typing import Dict, Any, List

class HealthService:
    @staticmethod
    def classify_diet(ingredients: List[str]) -> str:
        """
        Provides a basic dietary classification based on ingredients.
        """
        lower_ingredients = [ing.lower() for ing in ingredients]
        
        meat_keywords = ["meat", "chicken", "beef", "pork", "fish", "shrimp", "lamb", "bacon", "steak", "turkey"]
        animal_byproducts = ["milk", "cheese", "egg", "butter", "cream", "whey", "casein", "honey", "mayonnaise"]
        
        has_meat = any(any(meat in ing for meat in meat_keywords) for ing in lower_ingredients)
        has_animal_byproducts = any(any(byprod in ing for byprod in animal_byproducts) for ing in lower_ingredients)
        
        if has_meat:
            return "non-vegetarian"
        elif has_animal_byproducts:
            return "vegetarian"
        else:
            # Assuming vegan if no meat or known animal byproducts are found in the list
            return "vegan"

    @staticmethod
    def evaluate_nutrition(nutrition: Dict[str, float]) -> List[str]:
        """
        Generates rule-based health recommendations based on macronutrients.
        """
        recommendations = []
        
        # Arbitrary thresholds for an MVP
        if nutrition.get("sugar", 0) > 15.0:
            recommendations.append("High sugar warning: Consider limiting portion size.")
            
        if nutrition.get("sodium", 0) > 800.0:
            recommendations.append("High sodium warning: Not recommended for individuals with high blood pressure.")
            
        if nutrition.get("fats", 0) > 20.0:
            recommendations.append("High fat warning: This item is calorie-dense.")
            
        if nutrition.get("protein", 0) > 15.0:
            recommendations.append("Protein rich note: Good source of protein.")
            
        if nutrition.get("fiber", 0) > 5.0:
            recommendations.append("High fiber: Good for digestion.")
            
        if not recommendations:
            recommendations.append("Balanced meal note: Nutritional values are within moderate ranges.")
            
        return recommendations
