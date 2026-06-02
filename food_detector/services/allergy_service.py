from typing import List, Dict, Any

class AllergyService:
    # Synonym intelligence maps allergen categories to related terms/ingredients
    ALLERGEN_MAP = {
        "milk": ["milk", "whey", "casein", "butter", "cream", "cheese", "lactose", "ghee", "yogurt"],
        "egg": ["egg", "albumin", "mayo", "mayonnaise", "meringue", "ovalbumin"],
        "peanuts": ["peanut", "groundnut", "peanut oil", "peanut butter"],
        "tree nuts": ["almond", "walnut", "pecan", "cashew", "pistachio", "macadamia", "hazelnut"],
        "soy": ["soy", "soybean", "soy lecithin", "soy protein", "tofu", "edamame", "miso"],
        "wheat": ["wheat", "bran", "graham", "semolina", "spelt"],
        "gluten": ["gluten", "semolina", "wheat", "barley", "rye", "flour", "malt"],
        "fish": ["fish", "salmon", "tuna", "cod", "tilapia", "anchovies"],
        "shellfish": ["shrimp", "crab", "lobster", "prawn", "crawfish", "mussels", "oysters"],
        "sesame": ["sesame", "tahini", "sesame oil", "sesame seed"]
    }

    @classmethod
    def analyze_allergies(cls, ingredients: List[str]) -> Dict[str, List[str]]:
        """
        Analyzes ingredients against the ALLERGEN_MAP to detect allergens.
        Returns a dictionary with detected allergens and warnings.
        """
        detected_allergens = set()
        warnings = []

        lower_ingredients = [ing.lower() for ing in ingredients]

        for allergen_category, synonyms in cls.ALLERGEN_MAP.items():
            for synonym in synonyms:
                # Check if the synonym is in any of the ingredients
                if any(synonym in ing for ing in lower_ingredients):
                    detected_allergens.add(allergen_category)
                    break # Break inner loop once the category is detected

        allergens_list = list(detected_allergens)
        if allergens_list:
            warnings.append(f"Warning: Contains common allergens ({', '.join(allergens_list)}).")
        else:
            warnings.append("No common allergens detected. Always verify with actual product labels.")

        return {
            "allergens_detected": allergens_list,
            "warnings": warnings
        }
