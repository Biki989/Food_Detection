"""
Comprehensive food nutrition and ingredient database.

Maps Food-101 model labels to realistic per-serving nutritional data
and typical ingredient lists. This enables accurate allergen detection
and meaningful nutrition display without requiring an external API key.

All values are approximate per standard serving and sourced from
USDA FoodData Central reference values.
"""

from typing import Dict, Any, Optional
from rapidfuzz import process, fuzz

# Nutrition values: per standard serving (varies by food type)
# calories (kcal), protein (g), carbohydrates (g), fats (g),
# fiber (g), sugar (g), sodium (mg)
# ingredients: typical ingredient list for allergen scanning

FOOD_DATABASE: Dict[str, Dict[str, Any]] = {

    "apple": {
        "calories": 52.0, "protein": 0.3, "carbohydrates": 14.0,
        "fats": 0.2, "fiber": 2.4, "sugar": 10.0, "sodium": 1.0,
        "ingredients": ["apple"]
    },
    "banana": {
        "calories": 89.0, "protein": 1.1, "carbohydrates": 23.0,
        "fats": 0.3, "fiber": 2.6, "sugar": 12.0, "sodium": 1.0,
        "ingredients": ["banana"]
    },
    "beef": {
        "calories": 250.0, "protein": 26.0, "carbohydrates": 0.0,
        "fats": 15.0, "fiber": 0.0, "sugar": 0.0, "sodium": 60.0,
        "ingredients": ["beef"]
    },
    "bread": {
        "calories": 265.0, "protein": 9.0, "carbohydrates": 49.0,
        "fats": 3.2, "fiber": 2.7, "sugar": 5.0, "sodium": 490.0,
        "ingredients": ["wheat flour", "yeast", "water", "salt"]
    },
    "broccoli": {
        "calories": 34.0, "protein": 2.8, "carbohydrates": 7.0,
        "fats": 0.4, "fiber": 2.6, "sugar": 1.7, "sodium": 33.0,
        "ingredients": ["broccoli"]
    },
    "butter": {
        "calories": 717.0, "protein": 0.9, "carbohydrates": 0.1,
        "fats": 81.0, "fiber": 0.0, "sugar": 0.1, "sodium": 643.0,
        "ingredients": ["butter"]
    },
    "carrot": {
        "calories": 41.0, "protein": 0.9, "carbohydrates": 10.0,
        "fats": 0.2, "fiber": 2.8, "sugar": 4.7, "sodium": 69.0,
        "ingredients": ["carrot"]
    },
    "cheese": {
        "calories": 402.0, "protein": 25.0, "carbohydrates": 1.3,
        "fats": 33.0, "fiber": 0.0, "sugar": 0.5, "sodium": 621.0,
        "ingredients": ["milk", "salt", "enzymes"]
    },
    "egg": {
        "calories": 143.0, "protein": 12.6, "carbohydrates": 0.7,
        "fats": 9.5, "fiber": 0.0, "sugar": 0.4, "sodium": 124.0,
        "ingredients": ["egg"]
    },
    "milk": {
        "calories": 61.0, "protein": 3.2, "carbohydrates": 4.8,
        "fats": 3.3, "fiber": 0.0, "sugar": 5.0, "sodium": 44.0,
        "ingredients": ["milk"]
    },
    "orange": {
        "calories": 47.0, "protein": 0.9, "carbohydrates": 12.0,
        "fats": 0.1, "fiber": 2.4, "sugar": 9.0, "sodium": 0.0,
        "ingredients": ["orange"]
    },
    "pork": {
        "calories": 242.0, "protein": 27.0, "carbohydrates": 0.0,
        "fats": 14.0, "fiber": 0.0, "sugar": 0.0, "sodium": 62.0,
        "ingredients": ["pork"]
    },
    "potato": {
        "calories": 77.0, "protein": 2.0, "carbohydrates": 17.0,
        "fats": 0.1, "fiber": 2.2, "sugar": 0.8, "sodium": 6.0,
        "ingredients": ["potato"]
    },
    "spinach": {
        "calories": 23.0, "protein": 2.9, "carbohydrates": 3.6,
        "fats": 0.4, "fiber": 2.2, "sugar": 0.4, "sodium": 79.0,
        "ingredients": ["spinach"]
    },
    "tomato": {
        "calories": 18.0, "protein": 0.9, "carbohydrates": 3.9,
        "fats": 0.2, "fiber": 1.2, "sugar": 2.6, "sodium": 5.0,
        "ingredients": ["tomato"]
    },

    # ─── A ───
    "apple_pie": {
        "calories": 296.0, "protein": 2.4, "carbohydrates": 43.0,
        "fats": 14.0, "fiber": 1.9, "sugar": 22.0, "sodium": 327.0,
        "ingredients": ["apple", "wheat flour", "butter", "sugar", "cinnamon", "nutmeg", "salt", "lemon juice"]
    },

    # ─── B ───
    "baby_back_ribs": {
        "calories": 390.0, "protein": 29.0, "carbohydrates": 8.0,
        "fats": 27.0, "fiber": 0.3, "sugar": 6.0, "sodium": 680.0,
        "ingredients": ["pork ribs", "barbecue sauce", "brown sugar", "paprika", "garlic", "onion powder", "salt", "pepper"]
    },
    "baklava": {
        "calories": 334.0, "protein": 5.0, "carbohydrates": 29.0,
        "fats": 23.0, "fiber": 1.8, "sugar": 18.0, "sodium": 165.0,
        "ingredients": ["phyllo dough", "wheat flour", "butter", "pistachio", "walnut", "sugar", "honey", "cinnamon", "cardamom"]
    },
    "beef_carpaccio": {
        "calories": 180.0, "protein": 22.0, "carbohydrates": 2.0,
        "fats": 10.0, "fiber": 0.5, "sugar": 0.5, "sodium": 320.0,
        "ingredients": ["beef tenderloin", "olive oil", "lemon juice", "arugula", "capers", "parmesan cheese", "salt", "pepper"]
    },
    "beef_tartare": {
        "calories": 210.0, "protein": 24.0, "carbohydrates": 2.5,
        "fats": 12.0, "fiber": 0.3, "sugar": 0.5, "sodium": 380.0,
        "ingredients": ["beef", "egg yolk", "capers", "cornichons", "shallot", "dijon mustard", "worcestershire sauce", "tabasco", "salt", "pepper"]
    },
    "beet_salad": {
        "calories": 140.0, "protein": 4.5, "carbohydrates": 14.0,
        "fats": 8.0, "fiber": 3.0, "sugar": 9.0, "sodium": 290.0,
        "ingredients": ["beet", "goat cheese", "walnut", "arugula", "olive oil", "balsamic vinegar", "salt", "pepper"]
    },
    "beignets": {
        "calories": 350.0, "protein": 5.0, "carbohydrates": 42.0,
        "fats": 18.0, "fiber": 0.8, "sugar": 16.0, "sodium": 410.0,
        "ingredients": ["wheat flour", "egg", "milk", "butter", "sugar", "powdered sugar", "yeast", "salt", "vegetable oil"]
    },
    "bibimbap": {
        "calories": 490.0, "protein": 22.0, "carbohydrates": 65.0,
        "fats": 15.0, "fiber": 4.0, "sugar": 5.0, "sodium": 820.0,
        "ingredients": ["rice", "beef", "egg", "spinach", "carrot", "zucchini", "bean sprouts", "gochujang", "sesame oil", "soy sauce", "garlic"]
    },
    "bread_pudding": {
        "calories": 320.0, "protein": 8.0, "carbohydrates": 45.0,
        "fats": 12.0, "fiber": 1.0, "sugar": 28.0, "sodium": 350.0,
        "ingredients": ["bread", "wheat flour", "milk", "egg", "butter", "sugar", "vanilla", "cinnamon", "raisins", "cream"]
    },
    "breakfast_burrito": {
        "calories": 450.0, "protein": 20.0, "carbohydrates": 40.0,
        "fats": 24.0, "fiber": 3.0, "sugar": 3.0, "sodium": 870.0,
        "ingredients": ["wheat flour tortilla", "egg", "cheese", "sausage", "bell pepper", "onion", "salsa", "salt", "pepper"]
    },
    "bruschetta": {
        "calories": 180.0, "protein": 5.0, "carbohydrates": 22.0,
        "fats": 8.0, "fiber": 2.0, "sugar": 3.5, "sodium": 350.0,
        "ingredients": ["bread", "wheat flour", "tomato", "garlic", "basil", "olive oil", "balsamic vinegar", "salt", "pepper"]
    },

    # ─── C ───
    "caesar_salad": {
        "calories": 220.0, "protein": 8.0, "carbohydrates": 12.0,
        "fats": 16.0, "fiber": 2.5, "sugar": 2.0, "sodium": 540.0,
        "ingredients": ["romaine lettuce", "parmesan cheese", "croutons", "wheat flour", "egg yolk", "anchovy", "garlic", "olive oil", "lemon juice", "dijon mustard", "worcestershire sauce"]
    },
    "cannoli": {
        "calories": 370.0, "protein": 8.0, "carbohydrates": 38.0,
        "fats": 21.0, "fiber": 0.5, "sugar": 22.0, "sodium": 180.0,
        "ingredients": ["wheat flour", "ricotta cheese", "sugar", "powdered sugar", "chocolate chips", "butter", "egg", "vanilla", "cinnamon", "vegetable oil"]
    },
    "caprese_salad": {
        "calories": 250.0, "protein": 14.0, "carbohydrates": 5.0,
        "fats": 20.0, "fiber": 1.2, "sugar": 3.5, "sodium": 420.0,
        "ingredients": ["mozzarella cheese", "tomato", "basil", "olive oil", "balsamic vinegar", "salt", "pepper"]
    },
    "carrot_cake": {
        "calories": 415.0, "protein": 5.0, "carbohydrates": 52.0,
        "fats": 22.0, "fiber": 1.5, "sugar": 35.0, "sodium": 320.0,
        "ingredients": ["carrot", "wheat flour", "egg", "sugar", "vegetable oil", "walnut", "cream cheese", "butter", "cinnamon", "nutmeg", "baking soda", "vanilla"]
    },
    "ceviche": {
        "calories": 150.0, "protein": 18.0, "carbohydrates": 8.0,
        "fats": 5.0, "fiber": 1.5, "sugar": 3.0, "sodium": 480.0,
        "ingredients": ["fish", "shrimp", "lime juice", "lemon juice", "onion", "cilantro", "tomato", "jalapeño", "avocado", "salt", "pepper"]
    },
    "cheese_plate": {
        "calories": 380.0, "protein": 18.0, "carbohydrates": 8.0,
        "fats": 30.0, "fiber": 1.0, "sugar": 3.0, "sodium": 620.0,
        "ingredients": ["cheddar cheese", "brie cheese", "gouda cheese", "grapes", "crackers", "wheat flour", "walnut", "honey", "fig"]
    },
    "cheesecake": {
        "calories": 401.0, "protein": 7.0, "carbohydrates": 36.0,
        "fats": 26.0, "fiber": 0.4, "sugar": 26.0, "sodium": 310.0,
        "ingredients": ["cream cheese", "sugar", "egg", "sour cream", "vanilla", "butter", "graham cracker crust", "wheat flour"]
    },
    "chicken_curry": {
        "calories": 320.0, "protein": 25.0, "carbohydrates": 12.0,
        "fats": 20.0, "fiber": 2.5, "sugar": 4.0, "sodium": 720.0,
        "ingredients": ["chicken", "onion", "tomato", "coconut milk", "ginger", "garlic", "turmeric", "cumin", "coriander", "chili powder", "garam masala", "vegetable oil", "salt"]
    },
    "chicken_quesadilla": {
        "calories": 470.0, "protein": 28.0, "carbohydrates": 36.0,
        "fats": 24.0, "fiber": 2.0, "sugar": 2.0, "sodium": 890.0,
        "ingredients": ["wheat flour tortilla", "chicken", "cheese", "bell pepper", "onion", "sour cream", "salsa", "vegetable oil", "salt", "pepper"]
    },
    "chicken_wings": {
        "calories": 430.0, "protein": 30.0, "carbohydrates": 6.0,
        "fats": 32.0, "fiber": 0.5, "sugar": 2.0, "sodium": 1050.0,
        "ingredients": ["chicken wings", "butter", "hot sauce", "garlic", "vegetable oil", "salt", "pepper", "celery"]
    },
    "chocolate_cake": {
        "calories": 440.0, "protein": 5.0, "carbohydrates": 56.0,
        "fats": 23.0, "fiber": 2.0, "sugar": 40.0, "sodium": 390.0,
        "ingredients": ["wheat flour", "cocoa powder", "chocolate", "sugar", "egg", "butter", "milk", "baking soda", "vanilla", "salt", "cream"]
    },
    "chocolate_mousse": {
        "calories": 310.0, "protein": 5.0, "carbohydrates": 28.0,
        "fats": 22.0, "fiber": 1.5, "sugar": 24.0, "sodium": 55.0,
        "ingredients": ["chocolate", "cream", "egg", "sugar", "butter", "vanilla", "cocoa powder"]
    },
    "churros": {
        "calories": 280.0, "protein": 3.5, "carbohydrates": 32.0,
        "fats": 16.0, "fiber": 0.8, "sugar": 14.0, "sodium": 210.0,
        "ingredients": ["wheat flour", "butter", "egg", "sugar", "cinnamon", "vegetable oil", "salt", "vanilla", "chocolate sauce"]
    },
    "clam_chowder": {
        "calories": 260.0, "protein": 10.0, "carbohydrates": 22.0,
        "fats": 15.0, "fiber": 1.2, "sugar": 2.5, "sodium": 890.0,
        "ingredients": ["clam", "potato", "onion", "celery", "cream", "milk", "butter", "wheat flour", "bacon", "garlic", "salt", "pepper", "thyme"]
    },
    "club_sandwich": {
        "calories": 520.0, "protein": 32.0, "carbohydrates": 35.0,
        "fats": 28.0, "fiber": 2.5, "sugar": 4.0, "sodium": 1150.0,
        "ingredients": ["bread", "wheat flour", "turkey", "bacon", "lettuce", "tomato", "mayonnaise", "egg", "cheese", "salt", "pepper"]
    },
    "crab_cakes": {
        "calories": 280.0, "protein": 18.0, "carbohydrates": 12.0,
        "fats": 18.0, "fiber": 0.5, "sugar": 1.5, "sodium": 620.0,
        "ingredients": ["crab", "breadcrumbs", "wheat flour", "egg", "mayonnaise", "mustard", "worcestershire sauce", "bell pepper", "onion", "parsley", "salt", "pepper", "vegetable oil"]
    },
    "creme_brulee": {
        "calories": 330.0, "protein": 5.0, "carbohydrates": 28.0,
        "fats": 22.0, "fiber": 0.0, "sugar": 25.0, "sodium": 65.0,
        "ingredients": ["cream", "egg yolk", "sugar", "vanilla bean", "salt"]
    },
    "croque_madame": {
        "calories": 520.0, "protein": 26.0, "carbohydrates": 30.0,
        "fats": 33.0, "fiber": 1.5, "sugar": 3.0, "sodium": 1020.0,
        "ingredients": ["bread", "wheat flour", "ham", "gruyere cheese", "butter", "egg", "milk", "dijon mustard", "nutmeg", "salt", "pepper"]
    },
    "cup_cakes": {
        "calories": 350.0, "protein": 3.5, "carbohydrates": 50.0,
        "fats": 16.0, "fiber": 0.5, "sugar": 34.0, "sodium": 280.0,
        "ingredients": ["wheat flour", "sugar", "butter", "egg", "milk", "vanilla", "baking powder", "cream cheese frosting", "food coloring", "salt"]
    },

    # ─── D ───
    "deviled_eggs": {
        "calories": 130.0, "protein": 7.0, "carbohydrates": 1.0,
        "fats": 10.0, "fiber": 0.0, "sugar": 0.5, "sodium": 250.0,
        "ingredients": ["egg", "mayonnaise", "mustard", "paprika", "salt", "pepper", "vinegar"]
    },
    "donuts": {
        "calories": 380.0, "protein": 5.0, "carbohydrates": 45.0,
        "fats": 20.0, "fiber": 1.0, "sugar": 22.0, "sodium": 350.0,
        "ingredients": ["wheat flour", "sugar", "egg", "milk", "butter", "yeast", "vegetable oil", "vanilla", "salt", "glaze"]
    },
    "dumplings": {
        "calories": 260.0, "protein": 12.0, "carbohydrates": 30.0,
        "fats": 10.0, "fiber": 1.5, "sugar": 2.0, "sodium": 580.0,
        "ingredients": ["wheat flour", "pork", "cabbage", "ginger", "garlic", "soy sauce", "sesame oil", "green onion", "salt", "pepper"]
    },

    # ─── E ───
    "edamame": {
        "calories": 120.0, "protein": 11.0, "carbohydrates": 9.0,
        "fats": 5.0, "fiber": 4.0, "sugar": 2.0, "sodium": 6.0,
        "ingredients": ["soybean", "salt"]
    },
    "eggs_benedict": {
        "calories": 540.0, "protein": 24.0, "carbohydrates": 28.0,
        "fats": 38.0, "fiber": 1.0, "sugar": 2.5, "sodium": 1050.0,
        "ingredients": ["english muffin", "wheat flour", "egg", "canadian bacon", "butter", "lemon juice", "cayenne pepper", "salt", "vinegar"]
    },
    "escargots": {
        "calories": 220.0, "protein": 14.0, "carbohydrates": 3.0,
        "fats": 17.0, "fiber": 0.2, "sugar": 0.5, "sodium": 380.0,
        "ingredients": ["snail", "butter", "garlic", "parsley", "shallot", "white wine", "salt", "pepper"]
    },

    # ─── F ───
    "falafel": {
        "calories": 330.0, "protein": 13.0, "carbohydrates": 32.0,
        "fats": 18.0, "fiber": 5.0, "sugar": 3.0, "sodium": 580.0,
        "ingredients": ["chickpea", "onion", "garlic", "parsley", "cilantro", "cumin", "coriander", "wheat flour", "baking powder", "vegetable oil", "salt", "pepper"]
    },
    "filet_mignon": {
        "calories": 350.0, "protein": 40.0, "carbohydrates": 0.0,
        "fats": 20.0, "fiber": 0.0, "sugar": 0.0, "sodium": 380.0,
        "ingredients": ["beef tenderloin", "butter", "garlic", "thyme", "rosemary", "olive oil", "salt", "pepper"]
    },
    "fish_and_chips": {
        "calories": 580.0, "protein": 25.0, "carbohydrates": 55.0,
        "fats": 30.0, "fiber": 3.5, "sugar": 2.0, "sodium": 750.0,
        "ingredients": ["cod fish", "potato", "wheat flour", "beer", "egg", "vegetable oil", "malt vinegar", "salt", "pepper", "baking powder"]
    },
    "foie_gras": {
        "calories": 460.0, "protein": 11.0, "carbohydrates": 4.0,
        "fats": 44.0, "fiber": 0.0, "sugar": 1.0, "sodium": 520.0,
        "ingredients": ["duck liver", "salt", "pepper", "cognac", "butter", "truffle"]
    },
    "french_fries": {
        "calories": 365.0, "protein": 4.0, "carbohydrates": 48.0,
        "fats": 17.0, "fiber": 4.0, "sugar": 0.5, "sodium": 320.0,
        "ingredients": ["potato", "vegetable oil", "salt"]
    },
    "french_onion_soup": {
        "calories": 290.0, "protein": 12.0, "carbohydrates": 22.0,
        "fats": 16.0, "fiber": 2.0, "sugar": 6.0, "sodium": 980.0,
        "ingredients": ["onion", "beef broth", "gruyere cheese", "bread", "wheat flour", "butter", "white wine", "thyme", "bay leaf", "salt", "pepper"]
    },
    "french_toast": {
        "calories": 340.0, "protein": 10.0, "carbohydrates": 36.0,
        "fats": 17.0, "fiber": 1.0, "sugar": 14.0, "sodium": 440.0,
        "ingredients": ["bread", "wheat flour", "egg", "milk", "butter", "cinnamon", "vanilla", "maple syrup", "powdered sugar", "salt"]
    },
    "fried_calamari": {
        "calories": 300.0, "protein": 15.0, "carbohydrates": 22.0,
        "fats": 17.0, "fiber": 1.0, "sugar": 1.5, "sodium": 620.0,
        "ingredients": ["squid", "wheat flour", "cornmeal", "egg", "milk", "garlic", "lemon", "vegetable oil", "marinara sauce", "salt", "pepper"]
    },
    "fried_rice": {
        "calories": 340.0, "protein": 10.0, "carbohydrates": 48.0,
        "fats": 12.0, "fiber": 2.0, "sugar": 3.0, "sodium": 820.0,
        "ingredients": ["rice", "egg", "soy sauce", "green onion", "peas", "carrot", "garlic", "sesame oil", "vegetable oil", "salt", "pepper"]
    },
    "frozen_yogurt": {
        "calories": 220.0, "protein": 6.0, "carbohydrates": 38.0,
        "fats": 5.0, "fiber": 0.5, "sugar": 30.0, "sodium": 100.0,
        "ingredients": ["yogurt", "milk", "sugar", "cream", "vanilla", "fruit", "gelatin"]
    },

    # ─── G ───
    "garlic_bread": {
        "calories": 260.0, "protein": 5.0, "carbohydrates": 28.0,
        "fats": 14.0, "fiber": 1.5, "sugar": 2.0, "sodium": 480.0,
        "ingredients": ["bread", "wheat flour", "butter", "garlic", "parsley", "parmesan cheese", "olive oil", "salt"]
    },
    "gnocchi": {
        "calories": 310.0, "protein": 7.0, "carbohydrates": 45.0,
        "fats": 10.0, "fiber": 2.5, "sugar": 3.0, "sodium": 520.0,
        "ingredients": ["potato", "wheat flour", "egg", "parmesan cheese", "butter", "sage", "nutmeg", "salt"]
    },
    "greek_salad": {
        "calories": 200.0, "protein": 6.0, "carbohydrates": 10.0,
        "fats": 15.0, "fiber": 3.0, "sugar": 5.0, "sodium": 520.0,
        "ingredients": ["cucumber", "tomato", "red onion", "feta cheese", "olive", "olive oil", "oregano", "red wine vinegar", "bell pepper", "salt", "pepper"]
    },
    "grilled_cheese_sandwich": {
        "calories": 440.0, "protein": 16.0, "carbohydrates": 30.0,
        "fats": 28.0, "fiber": 1.5, "sugar": 4.0, "sodium": 780.0,
        "ingredients": ["bread", "wheat flour", "cheddar cheese", "butter", "salt"]
    },
    "grilled_salmon": {
        "calories": 310.0, "protein": 34.0, "carbohydrates": 0.0,
        "fats": 18.0, "fiber": 0.0, "sugar": 0.0, "sodium": 380.0,
        "ingredients": ["salmon", "olive oil", "lemon juice", "garlic", "dill", "salt", "pepper"]
    },
    "guacamole": {
        "calories": 160.0, "protein": 2.0, "carbohydrates": 9.0,
        "fats": 14.0, "fiber": 6.5, "sugar": 1.0, "sodium": 310.0,
        "ingredients": ["avocado", "lime juice", "onion", "tomato", "cilantro", "jalapeño", "garlic", "salt", "pepper"]
    },
    "gyoza": {
        "calories": 250.0, "protein": 11.0, "carbohydrates": 28.0,
        "fats": 10.0, "fiber": 1.5, "sugar": 2.0, "sodium": 550.0,
        "ingredients": ["wheat flour", "pork", "cabbage", "ginger", "garlic", "soy sauce", "sesame oil", "green onion", "rice vinegar", "salt"]
    },

    # ─── H ───
    "hamburger": {
        "calories": 540.0, "protein": 28.0, "carbohydrates": 40.0,
        "fats": 30.0, "fiber": 2.0, "sugar": 8.0, "sodium": 820.0,
        "ingredients": ["beef patty", "hamburger bun", "wheat flour", "lettuce", "tomato", "onion", "pickles", "ketchup", "mustard", "cheese", "salt", "pepper"]
    },
    "hot_and_sour_soup": {
        "calories": 130.0, "protein": 8.0, "carbohydrates": 10.0,
        "fats": 6.0, "fiber": 1.5, "sugar": 2.0, "sodium": 920.0,
        "ingredients": ["tofu", "soy sauce", "mushroom", "bamboo shoots", "egg", "rice vinegar", "sesame oil", "white pepper", "cornstarch", "chili oil", "green onion"]
    },
    "hot_dog": {
        "calories": 370.0, "protein": 13.0, "carbohydrates": 28.0,
        "fats": 22.0, "fiber": 1.0, "sugar": 5.0, "sodium": 970.0,
        "ingredients": ["beef frankfurter", "pork", "hot dog bun", "wheat flour", "ketchup", "mustard", "relish", "onion", "salt"]
    },
    "huevos_rancheros": {
        "calories": 380.0, "protein": 18.0, "carbohydrates": 32.0,
        "fats": 20.0, "fiber": 5.0, "sugar": 4.0, "sodium": 750.0,
        "ingredients": ["egg", "corn tortilla", "tomato", "onion", "jalapeño", "garlic", "black beans", "cheese", "avocado", "cilantro", "cumin", "vegetable oil", "salt"]
    },
    "hummus": {
        "calories": 180.0, "protein": 8.0, "carbohydrates": 16.0,
        "fats": 10.0, "fiber": 4.0, "sugar": 1.0, "sodium": 380.0,
        "ingredients": ["chickpea", "tahini", "sesame", "lemon juice", "garlic", "olive oil", "cumin", "salt", "paprika"]
    },

    # ─── I ───
    "ice_cream": {
        "calories": 270.0, "protein": 5.0, "carbohydrates": 32.0,
        "fats": 14.0, "fiber": 0.5, "sugar": 28.0, "sodium": 80.0,
        "ingredients": ["cream", "milk", "sugar", "egg yolk", "vanilla", "salt"]
    },

    # ─── L ───
    "lasagna": {
        "calories": 420.0, "protein": 22.0, "carbohydrates": 35.0,
        "fats": 22.0, "fiber": 2.5, "sugar": 6.0, "sodium": 830.0,
        "ingredients": ["lasagna noodles", "wheat flour", "egg", "beef", "tomato sauce", "ricotta cheese", "mozzarella cheese", "parmesan cheese", "onion", "garlic", "basil", "oregano", "olive oil", "salt", "pepper"]
    },
    "lobster_bisque": {
        "calories": 290.0, "protein": 15.0, "carbohydrates": 12.0,
        "fats": 20.0, "fiber": 0.5, "sugar": 3.0, "sodium": 850.0,
        "ingredients": ["lobster", "cream", "butter", "wheat flour", "onion", "celery", "carrot", "tomato paste", "sherry wine", "garlic", "bay leaf", "salt", "pepper"]
    },
    "lobster_roll_sandwich": {
        "calories": 420.0, "protein": 22.0, "carbohydrates": 26.0,
        "fats": 26.0, "fiber": 1.0, "sugar": 3.0, "sodium": 720.0,
        "ingredients": ["lobster", "hot dog bun", "wheat flour", "butter", "mayonnaise", "lemon juice", "celery", "chives", "salt", "pepper"]
    },

    # ─── M ───
    "macaroni_and_cheese": {
        "calories": 410.0, "protein": 15.0, "carbohydrates": 40.0,
        "fats": 22.0, "fiber": 1.5, "sugar": 4.0, "sodium": 720.0,
        "ingredients": ["macaroni", "wheat flour", "cheddar cheese", "milk", "butter", "cream", "mustard powder", "nutmeg", "salt", "pepper"]
    },
    "macarons": {
        "calories": 180.0, "protein": 3.5, "carbohydrates": 28.0,
        "fats": 7.0, "fiber": 1.0, "sugar": 24.0, "sodium": 30.0,
        "ingredients": ["almond flour", "powdered sugar", "egg white", "sugar", "cream", "butter", "vanilla", "food coloring"]
    },
    "miso_soup": {
        "calories": 65.0, "protein": 5.0, "carbohydrates": 5.0,
        "fats": 2.5, "fiber": 1.0, "sugar": 1.5, "sodium": 870.0,
        "ingredients": ["miso paste", "soybean", "tofu", "seaweed", "green onion", "dashi stock", "fish"]
    },
    "mussels": {
        "calories": 250.0, "protein": 20.0, "carbohydrates": 8.0,
        "fats": 12.0, "fiber": 0.5, "sugar": 2.0, "sodium": 640.0,
        "ingredients": ["mussels", "garlic", "shallot", "white wine", "butter", "cream", "parsley", "bread", "wheat flour", "salt", "pepper"]
    },

    # ─── N ───
    "nachos": {
        "calories": 520.0, "protein": 18.0, "carbohydrates": 48.0,
        "fats": 30.0, "fiber": 5.0, "sugar": 3.0, "sodium": 1100.0,
        "ingredients": ["corn tortilla chips", "cheddar cheese", "jalapeño", "sour cream", "guacamole", "avocado", "salsa", "tomato", "onion", "black beans", "ground beef", "salt"]
    },

    # ─── O ───
    "omelette": {
        "calories": 310.0, "protein": 20.0, "carbohydrates": 2.0,
        "fats": 24.0, "fiber": 0.5, "sugar": 1.0, "sodium": 480.0,
        "ingredients": ["egg", "butter", "cheese", "milk", "bell pepper", "mushroom", "onion", "ham", "salt", "pepper"]
    },
    "onion_rings": {
        "calories": 400.0, "protein": 5.0, "carbohydrates": 45.0,
        "fats": 22.0, "fiber": 2.0, "sugar": 5.0, "sodium": 520.0,
        "ingredients": ["onion", "wheat flour", "egg", "milk", "breadcrumbs", "vegetable oil", "salt", "pepper", "paprika"]
    },
    "oysters": {
        "calories": 110.0, "protein": 12.0, "carbohydrates": 6.0,
        "fats": 4.0, "fiber": 0.0, "sugar": 0.5, "sodium": 310.0,
        "ingredients": ["oysters", "lemon juice", "cocktail sauce", "horseradish", "tabasco", "salt"]
    },

    # ─── P ───
    "pad_thai": {
        "calories": 420.0, "protein": 16.0, "carbohydrates": 50.0,
        "fats": 18.0, "fiber": 2.0, "sugar": 10.0, "sodium": 880.0,
        "ingredients": ["rice noodles", "shrimp", "tofu", "egg", "peanut", "bean sprouts", "green onion", "lime", "fish sauce", "tamarind paste", "sugar", "garlic", "chili flakes", "vegetable oil"]
    },
    "paella": {
        "calories": 450.0, "protein": 26.0, "carbohydrates": 48.0,
        "fats": 16.0, "fiber": 2.5, "sugar": 3.0, "sodium": 780.0,
        "ingredients": ["rice", "shrimp", "mussels", "chicken", "chorizo sausage", "tomato", "bell pepper", "onion", "garlic", "saffron", "olive oil", "peas", "lemon", "salt", "pepper"]
    },
    "pancakes": {
        "calories": 350.0, "protein": 8.0, "carbohydrates": 48.0,
        "fats": 14.0, "fiber": 1.0, "sugar": 14.0, "sodium": 560.0,
        "ingredients": ["wheat flour", "egg", "milk", "butter", "sugar", "baking powder", "maple syrup", "vanilla", "salt"]
    },
    "panna_cotta": {
        "calories": 280.0, "protein": 4.0, "carbohydrates": 24.0,
        "fats": 19.0, "fiber": 0.0, "sugar": 22.0, "sodium": 45.0,
        "ingredients": ["cream", "milk", "sugar", "vanilla", "gelatin"]
    },
    "peking_duck": {
        "calories": 380.0, "protein": 22.0, "carbohydrates": 18.0,
        "fats": 24.0, "fiber": 1.0, "sugar": 8.0, "sodium": 680.0,
        "ingredients": ["duck", "wheat flour pancake", "hoisin sauce", "soy sauce", "cucumber", "green onion", "sugar", "five spice", "ginger", "salt"]
    },
    "pho": {
        "calories": 380.0, "protein": 22.0, "carbohydrates": 42.0,
        "fats": 12.0, "fiber": 2.0, "sugar": 4.0, "sodium": 1150.0,
        "ingredients": ["rice noodles", "beef", "beef broth", "onion", "ginger", "star anise", "cinnamon", "fish sauce", "bean sprouts", "basil", "lime", "jalapeño", "hoisin sauce", "sriracha"]
    },
    "pizza": {
        "calories": 400.0, "protein": 16.0, "carbohydrates": 42.0,
        "fats": 18.0, "fiber": 2.5, "sugar": 5.0, "sodium": 840.0,
        "ingredients": ["wheat flour", "mozzarella cheese", "tomato sauce", "olive oil", "yeast", "sugar", "basil", "oregano", "garlic", "salt", "pepperoni"]
    },
    "pork_chop": {
        "calories": 340.0, "protein": 36.0, "carbohydrates": 0.0,
        "fats": 20.0, "fiber": 0.0, "sugar": 0.0, "sodium": 400.0,
        "ingredients": ["pork chop", "olive oil", "garlic", "rosemary", "thyme", "butter", "salt", "pepper"]
    },
    "poutine": {
        "calories": 510.0, "protein": 12.0, "carbohydrates": 50.0,
        "fats": 30.0, "fiber": 4.0, "sugar": 2.0, "sodium": 920.0,
        "ingredients": ["potato", "cheese curds", "gravy", "vegetable oil", "wheat flour", "butter", "beef broth", "salt", "pepper"]
    },
    "prime_rib": {
        "calories": 450.0, "protein": 38.0, "carbohydrates": 0.0,
        "fats": 32.0, "fiber": 0.0, "sugar": 0.0, "sodium": 480.0,
        "ingredients": ["beef rib roast", "garlic", "rosemary", "thyme", "olive oil", "butter", "salt", "pepper", "horseradish"]
    },
    "pulled_pork_sandwich": {
        "calories": 480.0, "protein": 28.0, "carbohydrates": 42.0,
        "fats": 22.0, "fiber": 2.0, "sugar": 14.0, "sodium": 950.0,
        "ingredients": ["pork shoulder", "hamburger bun", "wheat flour", "barbecue sauce", "brown sugar", "apple cider vinegar", "paprika", "garlic", "onion", "cumin", "salt", "pepper"]
    },

    # ─── R ───
    "ramen": {
        "calories": 450.0, "protein": 18.0, "carbohydrates": 52.0,
        "fats": 18.0, "fiber": 2.5, "sugar": 3.0, "sodium": 1350.0,
        "ingredients": ["wheat flour noodles", "pork broth", "pork belly", "soy sauce", "miso paste", "egg", "nori seaweed", "green onion", "bamboo shoots", "garlic", "ginger", "sesame oil", "salt"]
    },
    "ravioli": {
        "calories": 360.0, "protein": 14.0, "carbohydrates": 38.0,
        "fats": 16.0, "fiber": 2.0, "sugar": 5.0, "sodium": 620.0,
        "ingredients": ["wheat flour", "egg", "ricotta cheese", "parmesan cheese", "spinach", "tomato sauce", "garlic", "basil", "olive oil", "nutmeg", "salt", "pepper"]
    },
    "red_velvet_cake": {
        "calories": 410.0, "protein": 4.5, "carbohydrates": 50.0,
        "fats": 22.0, "fiber": 0.5, "sugar": 38.0, "sodium": 340.0,
        "ingredients": ["wheat flour", "cocoa powder", "sugar", "butter", "egg", "buttermilk", "milk", "red food coloring", "vanilla", "baking soda", "vinegar", "cream cheese frosting", "salt"]
    },
    "risotto": {
        "calories": 380.0, "protein": 10.0, "carbohydrates": 48.0,
        "fats": 14.0, "fiber": 1.5, "sugar": 2.0, "sodium": 620.0,
        "ingredients": ["arborio rice", "parmesan cheese", "butter", "onion", "garlic", "white wine", "chicken broth", "olive oil", "mushroom", "salt", "pepper"]
    },

    # ─── S ───
    "samosa": {
        "calories": 310.0, "protein": 6.0, "carbohydrates": 34.0,
        "fats": 16.0, "fiber": 3.0, "sugar": 2.0, "sodium": 420.0,
        "ingredients": ["wheat flour", "potato", "peas", "onion", "cumin", "coriander", "garam masala", "ginger", "chili", "vegetable oil", "salt", "cilantro"]
    },
    "sashimi": {
        "calories": 140.0, "protein": 26.0, "carbohydrates": 0.0,
        "fats": 4.0, "fiber": 0.0, "sugar": 0.0, "sodium": 280.0,
        "ingredients": ["salmon", "tuna", "soy sauce", "wasabi", "ginger", "daikon radish"]
    },
    "scallops": {
        "calories": 220.0, "protein": 20.0, "carbohydrates": 5.0,
        "fats": 12.0, "fiber": 0.3, "sugar": 1.0, "sodium": 450.0,
        "ingredients": ["scallops", "butter", "garlic", "lemon juice", "white wine", "parsley", "olive oil", "salt", "pepper"]
    },
    "seaweed_salad": {
        "calories": 100.0, "protein": 2.0, "carbohydrates": 12.0,
        "fats": 5.0, "fiber": 2.5, "sugar": 5.0, "sodium": 680.0,
        "ingredients": ["seaweed", "sesame oil", "sesame seed", "rice vinegar", "soy sauce", "sugar", "chili flakes", "ginger"]
    },
    "shrimp_and_grits": {
        "calories": 420.0, "protein": 24.0, "carbohydrates": 30.0,
        "fats": 22.0, "fiber": 1.5, "sugar": 2.0, "sodium": 780.0,
        "ingredients": ["shrimp", "corn grits", "bacon", "cheddar cheese", "butter", "garlic", "lemon juice", "green onion", "chicken broth", "salt", "pepper"]
    },
    "spaghetti_bolognese": {
        "calories": 420.0, "protein": 22.0, "carbohydrates": 48.0,
        "fats": 16.0, "fiber": 3.5, "sugar": 8.0, "sodium": 680.0,
        "ingredients": ["spaghetti", "wheat flour", "beef", "tomato sauce", "onion", "carrot", "celery", "garlic", "red wine", "olive oil", "parmesan cheese", "basil", "oregano", "salt", "pepper"]
    },
    "spaghetti_carbonara": {
        "calories": 480.0, "protein": 20.0, "carbohydrates": 45.0,
        "fats": 24.0, "fiber": 2.0, "sugar": 2.0, "sodium": 720.0,
        "ingredients": ["spaghetti", "wheat flour", "egg", "pecorino cheese", "parmesan cheese", "pancetta", "black pepper", "garlic", "salt"]
    },
    "spring_rolls": {
        "calories": 200.0, "protein": 6.0, "carbohydrates": 26.0,
        "fats": 8.0, "fiber": 1.5, "sugar": 3.0, "sodium": 450.0,
        "ingredients": ["rice paper", "shrimp", "rice noodles", "lettuce", "carrot", "cucumber", "mint", "basil", "peanut", "hoisin sauce", "soy sauce"]
    },
    "steak": {
        "calories": 400.0, "protein": 38.0, "carbohydrates": 0.0,
        "fats": 26.0, "fiber": 0.0, "sugar": 0.0, "sodium": 420.0,
        "ingredients": ["beef steak", "olive oil", "butter", "garlic", "thyme", "rosemary", "salt", "pepper"]
    },
    "strawberry_shortcake": {
        "calories": 340.0, "protein": 4.0, "carbohydrates": 42.0,
        "fats": 18.0, "fiber": 2.0, "sugar": 26.0, "sodium": 280.0,
        "ingredients": ["strawberry", "wheat flour", "cream", "sugar", "butter", "egg", "milk", "baking powder", "vanilla", "salt"]
    },
    "sushi": {
        "calories": 280.0, "protein": 14.0, "carbohydrates": 38.0,
        "fats": 6.0, "fiber": 1.5, "sugar": 6.0, "sodium": 620.0,
        "ingredients": ["sushi rice", "nori seaweed", "salmon", "tuna", "avocado", "cucumber", "soy sauce", "rice vinegar", "sugar", "wasabi", "ginger", "sesame seed"]
    },

    # ─── T ───
    "tacos": {
        "calories": 370.0, "protein": 18.0, "carbohydrates": 28.0,
        "fats": 20.0, "fiber": 3.0, "sugar": 3.0, "sodium": 620.0,
        "ingredients": ["corn tortilla", "beef", "lettuce", "tomato", "cheese", "onion", "cilantro", "sour cream", "lime juice", "cumin", "chili powder", "garlic", "salt"]
    },
    "takoyaki": {
        "calories": 280.0, "protein": 10.0, "carbohydrates": 32.0,
        "fats": 12.0, "fiber": 1.0, "sugar": 4.0, "sodium": 650.0,
        "ingredients": ["wheat flour", "egg", "octopus", "dashi stock", "green onion", "pickled ginger", "takoyaki sauce", "mayonnaise", "bonito flakes", "fish", "nori seaweed", "vegetable oil"]
    },
    "tiramisu": {
        "calories": 370.0, "protein": 7.0, "carbohydrates": 34.0,
        "fats": 23.0, "fiber": 0.5, "sugar": 22.0, "sodium": 85.0,
        "ingredients": ["mascarpone cheese", "egg", "sugar", "espresso coffee", "ladyfinger biscuits", "wheat flour", "cocoa powder", "marsala wine", "vanilla"]
    },
    "tuna_tartare": {
        "calories": 180.0, "protein": 24.0, "carbohydrates": 4.0,
        "fats": 8.0, "fiber": 0.5, "sugar": 1.5, "sodium": 420.0,
        "ingredients": ["tuna", "avocado", "soy sauce", "sesame oil", "sesame seed", "lime juice", "ginger", "shallot", "chili", "cilantro", "salt"]
    },

    # ─── W ───
    "waffles": {
        "calories": 380.0, "protein": 8.0, "carbohydrates": 48.0,
        "fats": 16.0, "fiber": 1.0, "sugar": 12.0, "sodium": 520.0,
        "ingredients": ["wheat flour", "egg", "milk", "butter", "sugar", "baking powder", "vanilla", "maple syrup", "salt"]
    },
}

# ─── Additional common food aliases ───
# Maps common names and variations to the canonical Food-101 label
FOOD_ALIASES: Dict[str, str] = {
    "ribs": "baby_back_ribs",
    "bbq ribs": "baby_back_ribs",
    "beef steak": "steak",
    "sirloin": "steak",
    "ribeye": "prime_rib",
    "biryani": "fried_rice",
    "paneer tikka": "chicken_curry",
    "butter chicken": "chicken_curry",
    "curry": "chicken_curry",
    "burger": "hamburger",
    "cheeseburger": "hamburger",
    "salad": "greek_salad",
    "pasta": "spaghetti_bolognese",
    "noodles": "ramen",
    "fries": "french_fries",
    "sandwich": "club_sandwich",
    "cake": "chocolate_cake",
    "pie": "apple_pie",
    "soup": "clam_chowder",
    "wings": "chicken_wings",
    "eggs": "omelette",
    "toast": "french_toast",
    "wrap": "breakfast_burrito",
    "burrito": "breakfast_burrito",
    "quesadilla": "chicken_quesadilla",
    "donut": "donuts",
    "doughnut": "donuts",
    "cupcake": "cup_cakes",
    "cupcakes": "cup_cakes",
    "mac and cheese": "macaroni_and_cheese",
    "mac n cheese": "macaroni_and_cheese",
    "salmon": "grilled_salmon",
    "lobster": "lobster_bisque",
    "shrimp": "shrimp_and_grits",
    "spaghetti": "spaghetti_bolognese",
    "carbonara": "spaghetti_carbonara",
    "bolognese": "spaghetti_bolognese",
    "ice cream cone": "ice_cream",
    "gelato": "ice_cream",
    "pancake": "pancakes",
    "waffle": "waffles",
    "taco": "tacos",
    "dumpling": "dumplings",
    "roll": "spring_rolls",
    "spring roll": "spring_rolls",
    "muffin": "cup_cakes",
    "brownie": "chocolate_cake",
    "croissant": "bread_pudding",
    "fish": "grilled_salmon",
    "fish taco": "tacos",
    "fried chicken": "chicken_wings",
    "grilled chicken": "chicken_curry",
    "roast chicken": "chicken_curry",
    "lamb": "steak",
    "lamb chop": "pork_chop",
}


def lookup_food(food_name: str) -> Optional[Dict[str, Any]]:
    """
    Looks up nutrition and ingredient data for a given food name.

    Strategy:
    1. Direct match against the Food-101 canonical labels (underscored)
    2. Direct match against known aliases
    3. Fuzzy match against all known keys and aliases

    Returns None if no confident match is found.
    """
    if not food_name:
        return None

    # Normalize: lowercase, replace underscores/hyphens with spaces, strip
    normalized = food_name.strip().lower().replace("_", " ").replace("-", " ")
    # Also create underscore version for direct DB lookup
    underscored = normalized.replace(" ", "_")

    # 1. Direct match in database
    if underscored in FOOD_DATABASE:
        return FOOD_DATABASE[underscored]

    # 2. Direct alias match
    if normalized in FOOD_ALIASES:
        canonical = FOOD_ALIASES[normalized]
        if canonical in FOOD_DATABASE:
            return FOOD_DATABASE[canonical]

    # 3. Fuzzy match against DB keys and aliases
    all_keys = list(FOOD_DATABASE.keys())
    alias_keys = list(FOOD_ALIASES.keys())

    # Try DB keys first (replace underscores for better matching)
    db_display_keys = [k.replace("_", " ") for k in all_keys]
    best_match = process.extractOne(
        normalized,
        db_display_keys,
        scorer=fuzz.WRatio,
        score_cutoff=65
    )
    if best_match:
        matched_key = all_keys[db_display_keys.index(best_match[0])]
        return FOOD_DATABASE[matched_key]

    # Try alias keys
    best_alias = process.extractOne(
        normalized,
        alias_keys,
        scorer=fuzz.WRatio,
        score_cutoff=65
    )
    if best_alias:
        canonical = FOOD_ALIASES[best_alias[0]]
        if canonical in FOOD_DATABASE:
            return FOOD_DATABASE[canonical]

    return None
