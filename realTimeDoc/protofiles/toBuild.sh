python -m grpc_tools.protoc -Iprotofiles --python_out=protofiles --pyi_out=protofiles --grpc_python_out=protofiles protofiles/rtf.proto

# copy generated files to server and client
cp protofiles/rtf_pb2.py server/
cp protofiles/rtf_pb2_grpc.py server/
cp protofiles/rtf_pb2.pyi server/

cp protofiles/rtf_pb2.py client/
cp protofiles/rtf_pb2_grpc.py client/
cp protofiles/rtf_pb2.pyi client/

# rm -rf protofiles/*.py
# rm -rf protofiles/*.pyi