from pydantic import BaseModel


class LanguageModelMetaData(BaseModel):
    model_name: str
    model_version: Optional[str]
    model_runner: LLMInterface
    cached: bool = False


class LLMInterface():
    def __init__(self, model_type: str, load: bool = False):
        self.model_type = model_type
        self.loaded = load

        if model_type.lower() == "gpt4":
            pass
        elif model_type.lower() == "claude":
            pass
        elif model_type.lower() == "huggingface":
            pass
        else:
            raise ValueError(f"Model type {model_type} is not supported.")
    
    def prompt(self, text: str):
        pass

    def load(self):
        self.loaded = True
