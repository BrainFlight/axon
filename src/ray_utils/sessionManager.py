import ray 
from typing import Optional

@ray.remote
class SessionStateManager:
    def __init__(self):
        self.session_refs = {}
    
    async def add_session(self, model_name: str, session_ref: ray.ObjectRef) -> bool:
        self.session_refs[model_name] = session_ref
        return True
    
    def get_session(self, model_name: str) -> Optional[ray.ObjectRef]:
        return self.session_refs.get(model_name)
    
    async def remove_session(self, model_name: str) -> bool:
        if model_name in self.session_refs:
            ref = self.session_refs.pop(model_name)
            ray.cancel(ref, force=True)
            return True
        return False
    
    async def list_models(self) -> list:
        return list(self.session_refs.keys())
