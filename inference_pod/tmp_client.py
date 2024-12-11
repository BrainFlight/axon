import grpc
import sys
sys.path.append('inference_pod/src')
import src.inference_pb2
import src.inference_pb2_grpc

def run_inference_example():
    """Example client implementation."""
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = inference_pb2_grpc.InferenceServiceStub(channel)
        
        # Configure the model
        config_request = inference_pb2.ConfigRequest(
            model_name="bert-base-uncased",
            task="sentiment-analysis"
        )
        config_response = stub.ConfigureModel(config_request)
        print(f"Configuration response: {config_response.message}")
        
        if config_response.success:
            # Run inference
            inference_request = inference_pb2.InferenceRequest(
                input_text="I love using transformers for NLP tasks!"
            )
            inference_response = stub.RunInference(inference_request)
            print(f"Inference output: {inference_response.output}")
            print(f"Confidence: {inference_response.confidence}")

if __name__ == '__main__':
    run_inference_example()
