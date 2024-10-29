
class LLMInterface():
    def __init__(self, model_name: str = "gpt-4"):
        self.model_name = model_name
        
        if model_name == "gpt-4":
            pass
        elif model_name == "claude":
            pass
