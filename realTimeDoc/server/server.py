import grpc
from concurrent import futures
import rtf_pb2, rtf_pb2_grpc
import asyncio
import logging

# Set up logging
logging.basicConfig(filename="rtf.log", level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

mod = 1000

class RTFServiceServicer(rtf_pb2_grpc.RTFServiceServicer):
    def __init__(self):
        self.document_content = "hello!"
        self.change_number = 0
        self.clients = {}
        self.logs = {}
        self.logged_index = 0
        logging.info("RTFService initialized with document content: '%s'", self.document_content)

    def InitializeClient(self, request, context):
        content = rtf_pb2.DocumentContent(content=self.document_content, lastChange=self.change_number)
        logging.info("Client initialized with content: '%s' and last change: %d", self.document_content, self.change_number)
        return content
    
    def adjustPosition(self, client_last_change, change_position):
        current_abs_index = self.change_number if self.change_number >= client_last_change else self.change_number + mod
        adjustment = 0

        for change_index in range(client_last_change + 1, current_abs_index + 1):
            actual_index = change_index % mod
            current_change = self.logs[actual_index]
            
            # Corrected access to attributes
            if current_change.change_type == "insert" and current_change.position <= change_position:
                adjustment += 1
            elif current_change.change_type == "delete" and current_change.position < change_position:
                adjustment -= 1

        logging.debug("Adjusted position from %d to %d", change_position, change_position + adjustment)
        return change_position + adjustment

    def handleInsert(self, request):
        adjusted_position = self.adjustPosition(request.changeIndex, request.position)
        self.document_content = self.document_content[:adjusted_position] + request.charChange + self.document_content[adjusted_position:]
        self.change_number = (self.change_number + 1) % mod
        
        change = rtf_pb2.DocumentChange(
            client_id=request.client_id,
            change_type="insert",
            position=adjusted_position,
            charChange=request.charChange,
            changeIndex=self.change_number
        )

        self.logs[self.change_number % mod] = change
        logging.info("Handled insert: '%s' at position %d", request.charChange, adjusted_position)
        return change
    
    def handleDelete(self, request):
        adjusted_position = self.adjustPosition(request.changeIndex, request.position)
        self.document_content = self.document_content[:adjusted_position] + self.document_content[adjusted_position + 1:]
        self.change_number = (self.change_number + 1) % mod

        change = rtf_pb2.DocumentChange(
            client_id=request.client_id,
            change_type="delete",
            position=adjusted_position,
            charChange="",
            changeIndex=self.change_number
        )

        self.logs[self.change_number % mod] = change
        logging.info("Handled delete at position %d", adjusted_position)
        return change

    async def SyncChanges(self, request, context):
        logging.info("Client %s connected", request.client_id)
        client_id = request.client_id
        client_queue = asyncio.Queue()
        self.clients[client_id] = client_queue

        try:
            while True:
                change = await client_queue.get()
                yield change
                logging.debug("Yielded change to client %s: %s", client_id, change)
        except asyncio.CancelledError:
            logging.warning("Client %s disconnected", client_id)
            del self.clients[client_id]

    async def SendLocalChange(self, request, context):
        logging.info("Received change from client %s: %s", request.client_id, request)
        if request.change_type == "insert":
            change = self.handleInsert(request)
        elif request.change_type == "delete":
            change = self.handleDelete(request)

        # Broadcast the change to all connected clients asynchronously
        for client_id, client_queue in self.clients.items():
            await client_queue.put(change)

        logging.info("Broadcasted change to all clients: %s", change)
        return rtf_pb2.AckMessage(message="Change successfully broadcasted to all clients")

async def serve():
    server = grpc.aio.server() 
    rtf_pb2_grpc.add_RTFServiceServicer_to_server(RTFServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    logging.info("Starting gRPC server on port 50051")
    await server.start()
    await server.wait_for_termination()

if __name__ == "__main__":
    logging.info("Starting the RTF server...")
    asyncio.run(serve())
