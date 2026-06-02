# Food Nutrition & Allergy Detector

An AI-powered web application that analyzes a food photo or text input to provide nutritional information, detect potential allergens, and offer basic health recommendations.

## Features
- **Image Recognition**: Classifies food items from uploaded images using a pre-trained model.
- **Fuzzy Text Matching**: Handles typos and variations in manual text entries.
- **Nutritional Lookup**: Fetches detailed macronutrients and ingredients.
- **Allergen Detection**: Identifies common allergens based on ingredients.
- **Health Engine**: Provides rule-based dietary classifications and recommendations.

## Setup
1. Clone the repository.
2. Create a `.env` file based on `.env.example`.
3. Install dependencies: `pip install -r requirements.txt`
4. Run the server: `uvicorn app:app --reload`
