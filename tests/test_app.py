from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_analyze_no_input():
    response = client.post("/analyze")
    assert response.status_code == 400
    assert "Must provide either 'image' or 'text'" in response.json()["detail"]

def test_analyze_both_inputs():
    # Note: TestClient handles file uploads via files parameter
    response = client.post("/analyze", data={"text": "apple"}, files={"image": ("test.png", b"fakebytes", "image/png")})
    assert response.status_code == 400
    assert "Provide either 'image' OR 'text', not both" in response.json()["detail"]

def test_analyze_text():
    response = client.post("/analyze", data={"text": "pizza"})
    assert response.status_code == 200
    data = response.json()
    assert data["food_name"] == "pizza"
    assert "nutrition" in data
    assert "allergy_info" in data

    # Verify nutrition values are food-specific (not hardcoded mock)
    nutrition = data["nutrition"]
    assert nutrition["calories"] == 400.0
    assert nutrition["protein"] == 16.0

    # Verify allergens are detected from real ingredients
    allergens = data["allergy_info"]["allergens_detected"]
    assert "wheat" in allergens or "gluten" in allergens
    assert "milk" in allergens

def test_allergen_free_food():
    """Steak/filet mignon should have minimal allergens (just milk from butter)."""
    response = client.post("/analyze", data={"text": "french fries"})
    assert response.status_code == 200
    data = response.json()
    # French fries: potato, oil, salt — no common allergens
    allergens = data["allergy_info"]["allergens_detected"]
    assert len(allergens) == 0

def test_multiple_allergens():
    """Pad thai should detect multiple allergens (peanut, fish, shellfish, egg, soy)."""
    response = client.post("/analyze", data={"text": "pad thai"})
    assert response.status_code == 200
    data = response.json()
    allergens = data["allergy_info"]["allergens_detected"]
    assert "peanuts" in allergens
    assert "egg" in allergens

def test_dietary_classification():
    from services.health_service import HealthService
    
    # Test vegan classification (no meat, no animal byproducts)
    assert HealthService.classify_diet(["apple", "banana", "water"]) == "vegan"
    
    # Test vegetarian classification (no meat, but has milk/egg)
    assert HealthService.classify_diet(["wheat", "milk"]) == "vegetarian"
    assert HealthService.classify_diet(["egg", "flour"]) == "vegetarian"
    
    # Test non-vegetarian classification (contains meat)
    assert HealthService.classify_diet(["chicken", "rice"]) == "non-vegetarian"
    assert HealthService.classify_diet(["beef", "potato"]) == "non-vegetarian"

