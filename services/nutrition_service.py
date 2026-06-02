import os
import requests
from typing import Dict, Any, List

from services.food_database import lookup_food

class NutritionService:
    def __init__(self):
        api_key_env = os.getenv("USDA_API_KEY")
        self.api_key = api_key_env if api_key_env and api_key_env != "your_usda_api_key_here" else "DEMO_KEY"
        self.base_url = "https://api.nal.usda.gov/fdc/v1"

    def fetch_nutrition(self, food_name: str) -> Dict[str, Any]:
        """
        Fetches nutritional data for a given food name.

        Pipeline (falls through on failure):
          1. Local food database (covers all Food-101 labels + aliases)
          2. USDA FoodData Central API (if API key is configured)
          3. Generic fallback with food-name-aware estimation
        """

        # ── Step 1: Local database lookup ──
        local_data = lookup_food(food_name)
        if local_data is not None:
            return dict(local_data)  # return a copy to avoid mutation

        # ── Step 2: USDA API lookup ──
        if self.api_key:
            api_result = self._fetch_from_usda(food_name)
            if api_result is not None:
                return api_result

        # ── Step 3: Generic fallback ──
        return self._generic_fallback(food_name)

    def _fetch_from_usda(self, food_name: str) -> Dict[str, Any] | None:
        """
        Fetches from USDA FoodData Central API.
        Returns None on any failure so caller can fall through.
        """
        try:
            search_url = f"{self.base_url}/foods/search"
            params = {
                "api_key": self.api_key,
                "query": food_name,
                "pageSize": 1
            }
            response = requests.get(search_url, params=params, timeout=5)
            response.raise_for_status()
            data = response.json()

            if not data.get("foods"):
                return None

            food = data["foods"][0]
            nutrients = food.get("foodNutrients", [])

            def get_nutrient(name_substring: str) -> float:
                for n in nutrients:
                    if name_substring.lower() in n.get("nutrientName", "").lower():
                        return float(n.get("value", 0.0))
                return 0.0

            ingredients_str = food.get("ingredients", "")
            ingredients = [i.strip() for i in ingredients_str.split(",")] if ingredients_str else ["unknown"]

            return {
                "calories": get_nutrient("Energy"),
                "protein": get_nutrient("Protein"),
                "carbohydrates": get_nutrient("Carbohydrate"),
                "fats": get_nutrient("Total lipid"),
                "fiber": get_nutrient("Fiber"),
                "sugar": get_nutrient("Sugars"),
                "sodium": get_nutrient("Sodium"),
                "ingredients": ingredients
            }

        except Exception:
            return None

    def _generic_fallback(self, food_name: str) -> Dict[str, Any]:
        """
        Returns a best-effort generic estimation when the food isn't in
        the local database and the USDA API is unavailable.
        Uses the food name to infer basic ingredient categories.
        """
        name_lower = food_name.lower()

        # Try to infer likely ingredients from the food name
        ingredients = []

        # Protein sources
        if any(kw in name_lower for kw in ["chicken", "poultry", "hen"]):
            ingredients.append("chicken")
        if any(kw in name_lower for kw in ["beef", "steak", "burger", "meatball"]):
            ingredients.append("beef")
        if any(kw in name_lower for kw in ["pork", "ham", "bacon", "sausage"]):
            ingredients.append("pork")
        if any(kw in name_lower for kw in ["fish", "salmon", "tuna", "cod", "tilapia"]):
            ingredients.append("fish")
        if any(kw in name_lower for kw in ["shrimp", "prawn", "crab", "lobster"]):
            ingredients.append("shrimp")
        if any(kw in name_lower for kw in ["egg", "omelette", "frittata"]):
            ingredients.append("egg")

        # Common allergens
        if any(kw in name_lower for kw in ["cheese", "cream", "milk", "yogurt"]):
            ingredients.extend(["cheese", "milk"])
        if any(kw in name_lower for kw in ["bread", "toast", "sandwich", "pasta", "noodle", "cake", "pie", "cookie", "flour"]):
            ingredients.append("wheat flour")
        if any(kw in name_lower for kw in ["peanut"]):
            ingredients.append("peanut")
        if any(kw in name_lower for kw in ["almond", "walnut", "pecan", "cashew", "pistachio"]):
            ingredients.append("almond")
        if any(kw in name_lower for kw in ["soy", "tofu", "miso", "edamame"]):
            ingredients.append("soy sauce")
        if any(kw in name_lower for kw in ["sesame", "tahini"]):
            ingredients.append("sesame")

        if not ingredients:
            ingredients = [food_name]

        # Add common base ingredients
        ingredients.extend(["salt", "pepper"])

        # Heuristic nutrient estimation based on keywords
        calories = 150.0
        protein = 5.0
        carbs = 20.0
        fats = 5.0
        fiber = 1.0
        sugar = 2.0
        sodium = 200.0

        if any(kw in name_lower for kw in ["apple", "banana", "orange", "fruit", "grape", "berry", "peach", "pear", "plum"]):
            # Fruits
            calories = 60.0
            protein = 0.8
            carbs = 15.0
            fats = 0.2
            fiber = 2.5
            sugar = 10.0
            sodium = 2.0
        elif any(kw in name_lower for kw in ["chicken", "turkey", "poultry", "beef", "steak", "meat", "pork", "ham", "bacon"]):
            # Meats
            calories = 200.0
            protein = 28.0
            carbs = 0.0
            fats = 10.0
            fiber = 0.0
            sugar = 0.0
            sodium = 150.0
        elif any(kw in name_lower for kw in ["fish", "salmon", "tuna", "cod", "seafood", "shrimp"]):
            # Fish / Seafood
            calories = 160.0
            protein = 24.0
            carbs = 0.0
            fats = 6.0
            fiber = 0.0
            sugar = 0.0
            sodium = 200.0
        elif any(kw in name_lower for kw in ["cheese", "cream", "butter", "dairy", "yogurt", "milk"]):
            # Dairy
            calories = 180.0
            protein = 8.0
            carbs = 5.0
            fats = 14.0
            fiber = 0.0
            sugar = 4.0
            sodium = 300.0
        elif any(kw in name_lower for kw in ["bread", "toast", "sandwich", "pasta", "noodle", "rice", "grain", "flour"]):
            # Carbs/Grains
            calories = 220.0
            protein = 6.0
            carbs = 42.0
            fats = 2.5
            fiber = 2.0
            sugar = 2.0
            sodium = 350.0
        elif any(kw in name_lower for kw in ["salad", "broccoli", "spinach", "vegetable", "lettuce", "carrot", "tomato", "potato"]):
            # Vegetables
            calories = 80.0
            protein = 2.0
            carbs = 14.0
            fats = 1.0
            fiber = 3.0
            sugar = 3.0
            sodium = 100.0

        return {
            "calories": calories,
            "protein": protein,
            "carbohydrates": carbs,
            "fats": fats,
            "fiber": fiber,
            "sugar": sugar,
            "sodium": sodium,
            "ingredients": ingredients
        }
