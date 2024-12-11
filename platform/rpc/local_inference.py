# TODO: Replace inference_pb2 with local_inference_pb2 eventually

# rpc/inference_pod_client.py

import grpc
from typing import Optional, Tuple

from rpc.inference_pb2 import ConfigRequest, ConfigResponse, InferenceRequest, InferenceResponse
from rpc.inference_pb2_grpc import InferenceServiceStub

class InferencePodClient:
    """Client for interacting with the Inference Pod gRPC service."""
    
    def __init__(self, host: str = "localhost", port: int = 50051):
        """
        Initialize the client.
        
        Args:
            host: Hostname of the inference service
            port: Port number of the inference service
        """
        self.channel = grpc.insecure_channel(f"{host}:{port}")
        self.stub = InferenceServiceStub(self.channel)
        
    def __enter__(self):
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        
    def close(self):
        """Close the gRPC channel."""
        self.channel.close()
        
    def configure_model(self, model_name: str, task: str) -> Tuple[bool, str]:
        """
        Configure the model in the inference service.
        
        Args:
            model_name: Name of the Hugging Face model to load
            task: Type of task (e.g., 'text-generation', 'sentiment-analysis')
            
        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            request = ConfigRequest(model_name=model_name, task=task)
            response: ConfigResponse = self.stub.ConfigureModel(request)
            return response.success, response.message
        except grpc.RpcError as e:
            return False, f"RPC Error: {e.details()}"
            
    def run_inference(self, input_text: str) -> Tuple[Optional[str], Optional[float]]:
        """
        Run inference on the input text.
        
        Args:
            input_text: Input text for inference
            
        Returns:
            Tuple of (output: Optional[str], confidence: Optional[float])
        """
        try:
            request = InferenceRequest(input_text=input_text)
            response: InferenceResponse = self.stub.RunInference(request)
            return response.output, response.confidence
        except grpc.RpcError as e:
            return None, None
