import ray
from fastapi import FastAPI, Request
from ray import serve
import onnxruntime as ort
from ray_utils.sessionManager import SessionStateManager
import numpy as np
import os
import gc
from fastapi.exceptions import HTTPException
from pydantic import BaseModel
import logging 

app = FastAPI()

@serve.deployment()
@serve.ingress(app)
class ONNXModelDeployment:
    def __init__(self, model_directory: str):
        self.model_directory = model_directory
        self.model_manager = SessionStateManager.remote()
        self.logger = logging.getLogger(__name__)
    
    def _load_model(self, model_name: str):
        model_path = os.path.join(self.model_directory, model_name)
        self.logger.info(f"Loading model from {model_path}")
        path_ref = ray.put(model_path)
        self.logger.info(f"Path reference: {path_ref}")
        if type(path_ref) is ray.ObjectRef:
            success = self.model_manager.add_session.remote(model_name, path_ref)
            if success:
                return True
        
        return False
    
    @app.get("/v1/models")
    async def list_models(self):
        models = await self.model_manager.list_models.remote()
        return {"models": models}
    
    @app.post("/v1/models/{model_name}/load")
    async def load_model(self, model_name: str):
        success = self._load_model(model_name)
        if success:
            return {"message": "Model loaded successfully"}
        return {"message": f"Model loading failed for model {model_name}"}
    
    @app.post("/v1/models/{model_name}/unload")
    async def unload_model(self, model_name: str):
        success = await self.model_manager.remove_session.remote(model_name)
        if success:
            return {"message": "Model unloaded successfully"}
        return {"message": f"Model unloading failed for model {model_name}"}
    
    @app.post("/v1/models/{model_name}/inference")
    async def inference(self, model_name: str):
        session_ref = self.model_manager.get_session.remote(model_name)
        if session_ref is None:
            raise HTTPException(status_code=404, detail="Model not found")
        
        try:
            self.logger.info(f"Type for Session Reference: {type(session_ref)}")
            model_path = ray.get(session_ref)
            self.logger.info(f"Model path: {model_path}")
            return {"message": f"Model Path is {model_path}"}
        except Exception as e:
            self.logger.error(f"Error loading model: {e}")
            raise HTTPException(status_code=500, detail=f"Error loading model with session_ref: {session_ref}")
    
    

if __name__ == "__main__":
    import uvicorn

    # Initialize Ray and Serve
    ray.init(ignore_reinit_error=True)
    serve.start()

    # Define the model directory
    model_directory = "/path/to/model/directory"

    # Bind the deployment and run Serve
    deployment = ONNXModelDeployment.bind(model_directory)
    serve.run(deployment)

    # Start the FastAPI app with Uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info")