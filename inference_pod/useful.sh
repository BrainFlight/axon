
# Generate the gRPC code
python -m grpc_tools.protoc -I protos --python_out=src --grpc_python_out=src protos/inference.proto
