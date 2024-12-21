python -m grpc_tools.protoc -Iprotofiles --python_out=protofiles --pyi_out=protofiles --grpc_python_out=protofiles protofiles/labyrinth.proto

# copy generated files to server and client
cp protofiles/labyrinth_pb2.py server/
cp protofiles/labyrinth_pb2_grpc.py server/
cp protofiles/labyrinth_pb2.pyi server/

cp protofiles/labyrinth_pb2.py client/
cp protofiles/labyrinth_pb2_grpc.py client/
cp protofiles/labyrinth_pb2.pyi client/

# rm -rf protofiles/*.py
# rm -rf protofiles/*.pyi