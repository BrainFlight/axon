import grpc

import inference_pb2
import inference_pb2_grpc
from model_manager import ModelManager


class InferenceService(inference_pb2_grpc.InferenceServiceServicer):
    """gRPC service implementation for model inference."""

    def __init__(self):
        self.model_manager = ModelManager()

    def ConfigureModel(
        self, request: inference_pb2.ConfigRequest, context: grpc.ServicerContext
    ) -> inference_pb2.ConfigResponse:
        """Handle model configuration requests."""
        success, message = self.model_manager.configure_model(
            request.model_name, request.task
        )
        return inference_pb2.ConfigResponse(success=success, message=message)

    def RunInference(
        self, request: inference_pb2.InferenceRequest, context: grpc.ServicerContext
    ) -> inference_pb2.InferenceResponse:
        """Handle inference requests."""
        try:
            output, confidence = self.model_manager.run_inference(request.input_text)
            return inference_pb2.InferenceResponse(output=output, confidence=confidence)
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return inference_pb2.InferenceResponse()
