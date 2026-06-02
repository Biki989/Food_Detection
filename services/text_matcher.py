from rapidfuzz import process, fuzz
from typing import Optional, Tuple, List

from services.food_database import FOOD_DATABASE, FOOD_ALIASES

# Build the full list of known food names from the database and aliases
# Display names use spaces instead of underscores for better user matching
KNOWN_FOODS = [k.replace("_", " ") for k in FOOD_DATABASE.keys()]
KNOWN_FOODS.extend(FOOD_ALIASES.keys())
# Deduplicate while preserving order
KNOWN_FOODS = list(dict.fromkeys(KNOWN_FOODS))

class TextMatcherService:
    @staticmethod
    def normalize_food_name(user_input: str) -> str:
        """
        Normalizes the user input by trimming spaces and converting to lowercase.
        """
        return user_input.strip().lower()

    @staticmethod
    def fuzzy_match_food(user_input: str, threshold: float = 80.0) -> Tuple[Optional[str], float, List[str]]:
        """
        Uses rapidfuzz to find the closest matching known food name.
        Returns: (matched_name, confidence, top_3_predictions)
        """
        normalized = TextMatcherService.normalize_food_name(user_input)
        
        # Extract top 3 matches
        results = process.extract(
            normalized,
            KNOWN_FOODS,
            scorer=fuzz.token_sort_ratio,
            limit=3
        )
        
        if not results:
            return normalized, 100.0, [normalized]
            
        top_match = results[0]
        top_name, top_score = top_match[0], top_match[1]
        
        top_3 = [res[0] for res in results]
        
        if top_score >= threshold:
            return top_name, float(top_score / 100.0), top_3
        
        # Fallback to the original input if we aren't confident
        return normalized, 1.0, [normalized] + top_3[:2]
