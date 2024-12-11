from transformers import AutoModel, AutoTokenizer, pipeline
from typing import Optional, Tuple, Any

class ModelManager:
    """Manages the loading and inference of Hugging Face models."""
    
    def __init__(self):
        self.model = None
        self.pipeline = None
        self.task = None
    
    def configure_model(self, model_name: str, task: str) -> Tuple[bool, str]:
        """
        Configure the model and pipeline for inference.
        
        Args:
            model_name: Name of the Hugging Face model
            task: Type of task (e.g., 'text-generation', 'sentiment-analysis')
            
        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            self.pipeline = pipeline(task, model=model_name)
            self.task = task
            return True, f"Successfully loaded model {model_name} for {task}"
        except Exception as e:
            return False, f"Error loading model: {str(e)}"
    
    def run_inference(self, input_text: str) -> Tuple[str, float]:
        """
        Run inference on the input text.
        
        Args:
            input_text: Input text for inference
            
        Returns:
            Tuple of (output: str, confidence: float)
        """
        if not self.pipeline:
            raise RuntimeError("Model not configured. Call configure_model first.")
            
        result = self.pipeline(input_text)
        
        # Handle different output formats based on task
        if self.task == "text-generation":
            return result[0]["generated_text"], 1.0
        elif self.task == "sentiment-analysis":
            return result[0]["label"], result[0]["score"]
        else:
            # Generic handling for other tasks
            return str(result), 1.0
