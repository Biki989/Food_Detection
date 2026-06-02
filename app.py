from fastapi import FastAPI, File, UploadFile, Form, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import os
from dotenv import load_dotenv

from schemas.response_models import AnalyzeResponse
from services.text_matcher import TextMatcherService
from services.nutrition_service import NutritionService
from services.allergy_service import AllergyService
from services.health_service import HealthService
from services.image_detector import ImageDetectorService

load_dotenv()

app = FastAPI(
    title="Food Nutrition & Allergy Detector",
    description="API for detecting food from images or text and providing nutrition/allergy info.",
    version="1.0.0"
)

# Ensure required directories exist
# In Vercel, the filesystem is read-only except for /tmp
is_vercel = os.environ.get("VERCEL", "0") == "1"
upload_dir = "/tmp/uploads" if is_vercel else "uploads"
os.makedirs(upload_dir, exist_ok=True)
if not is_vercel:
    os.makedirs("static", exist_ok=True)

# Mount static and templates using absolute paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

# Initialize Services
# ImageDetectorService might take a while to download the model on the first run.
image_service = ImageDetectorService()
nutrition_service = NutritionService()

@app.get("/", response_class=HTMLResponse)
async def serve_frontend(request: Request):
    """Serves the minimal HTML skeleton for the frontend."""
    return templates.TemplateResponse(request=request, name="index.html")

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}

@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze_food(
    image: UploadFile = File(None),
    text: str = Form(None)
):
    """
    Main inference endpoint. 
    Accepts either an image upload or a text string.
    """
    if not image and not text:
        raise HTTPException(status_code=400, detail="Must provide either 'image' or 'text'.")
    
    if image and text:
        raise HTTPException(status_code=400, detail="Provide either 'image' OR 'text', not both.")

    food_name = "Unknown Food"
    confidence = 1.0
    top_predictions = []

    try:
        # PIPELINE LOGIC
        if image:
            # Check MIME type
            if not image.content_type.startswith("image/"):
                raise HTTPException(status_code=400, detail="Uploaded file is not an image.")
            
            image_bytes = await image.read()
            if not image_bytes:
                raise HTTPException(status_code=400, detail="Empty image file.")
                
            pred_name, conf, top_preds = image_service.predict(image_bytes)
            food_name = pred_name
            confidence = conf
            top_predictions = top_preds
            
        elif text:
            # Fuzzy match text
            pred_name, conf, top_preds = TextMatcherService.fuzzy_match_food(text)
            food_name = pred_name
            confidence = conf
            top_predictions = top_preds

        # Nutrition Lookup
        nutrition_data = nutrition_service.fetch_nutrition(food_name)
        ingredients = nutrition_data.get("ingredients", [])

        # Allergy Analysis
        allergy_info = AllergyService.analyze_allergies(ingredients)

        # Health Recommendation
        diet_class = HealthService.classify_diet(ingredients)
        health_recs = HealthService.evaluate_nutrition(nutrition_data)

        return {
            "food_name": food_name,
            "confidence": confidence,
            "top_predictions": top_predictions,
            "nutrition": nutrition_data,
            "allergy_info": allergy_info,
            "dietary_classification": diet_class,
            "health_recommendation": health_recs
        }
        
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
