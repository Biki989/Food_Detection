from PIL import Image
from typing import Tuple, List, Optional
import io

try:
    import torch
    from transformers import AutoImageProcessor, AutoModelForImageClassification
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False

class ImageDetectorService:
    def __init__(self):
        self.model_name = "nateraw/food"
        self.processor = None
        self.model = None
        if TORCH_AVAILABLE:
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
            self._load_model()
        else:
            self.device = "cpu"
            print("Warning: torch or transformers is not installed. Image detection is disabled.")

    def _load_model(self):
        """Loads the pre-trained food classification model."""
        if not TORCH_AVAILABLE:
            return
        try:
            self.processor = AutoImageProcessor.from_pretrained(self.model_name)
            self.model = AutoModelForImageClassification.from_pretrained(self.model_name)
            self.model.to(self.device)
            self.model.eval()
        except Exception as e:
            print(f"Warning: Failed to load model {self.model_name}. Error: {e}")

    def predict(self, image_bytes: bytes) -> Tuple[Optional[str], float, List[str]]:
        """
        Runs inference on the provided image bytes.
        Returns: (top_food_name, confidence, top_3_predictions)
        """
        if not TORCH_AVAILABLE:
            return "Image Detection Disabled", 0.0, ["Install PyTorch to enable image detection"]

        if not self.model or not self.processor:
            return "Model Not Loaded", 0.0, ["Model Not Loaded"]

        try:
            image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
            inputs = self.processor(images=image, return_tensors="pt").to(self.device)
            
            with torch.no_grad():
                outputs = self.model(**inputs)
                logits = outputs.logits
                
            # Get probabilities
            probabilities = torch.nn.functional.softmax(logits[0], dim=0)
            
            # Get top 3
            top3_prob, top3_indices = torch.topk(probabilities, 3)
            
            top3_predictions = []
            for i in range(3):
                idx = top3_indices[i].item()
                label = self.model.config.id2label[idx]
                top3_predictions.append(label)
                
            top_prediction = top3_predictions[0]
            confidence = top3_prob[0].item()
            
            return top_prediction, confidence, top3_predictions
            
        except Exception as e:
            print(f"Error during image prediction: {e}")
            return "Prediction Failed", 0.0, ["Prediction Failed"]
