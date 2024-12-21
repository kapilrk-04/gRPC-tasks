# Real-Time Collaborative Document Editing Application

# IMPORTANT NOTE - PARTIALLY IMPLEMENTED

Here, the server and client implementations are provided. The data written in the `curses` frontend is sent to the server and is broadcast to the other clients too, but due to time constraints there were certain issues in syncing the changes across different clients' frontends. The issue noted was:

```
protobuf gencodTask pending name='Task-4' coro=<StreamStreamCall._prepare_rpc() running at C:\Users\Kapil\anaconda3\lib\site-packages\grpc\aio\_call.py:751>> attached to a different loop 
```

Due to this, implementation could not be fully completed.

## Overview

This application enables real-time collaborative editing of a document using a curses-based client interface and a gRPC server. It allows multiple clients to connect to a server and edit a shared document simultaneously, with changes being synchronized across all connected clients.

## Architecture

The application consists of two main components:
1. **Client (`DocumentClient`)**: A curses-based interface that interacts with the user and communicates with the gRPC server.
2. **Server (`RTFServiceServicer`)**: A gRPC server that manages document content and synchronizes changes across clients.

## Requirements

- Python 3.x
- gRPC and Protobuf libraries
- `curses` module (typically included with standard Python installations)
- `logging` module (included with standard Python installations)
- `asyncio` module (included with standard Python installations)

## Client Implementation

### `DocumentClient`

This class handles the client-side logic for document editing.

#### Methods

- **`__init__()`**: Initializes the client with a random ID and an empty document.
- **`sync_changes()`**: Asynchronously listens for changes from the server and updates the local document.
- **`send_changes(change_type, char_change, position)`**: Sends a local change to the server.
- **`initialize_document()`**: Initializes the document content by fetching it from the server.
- **`run(stdscr)`**: Main loop that handles user input and updates the document in the curses interface.

### Key Functions in the Client

- **Input Handling**: The client captures keyboard inputs to perform actions like inserting and deleting characters, moving the cursor, and creating new lines.
- **Curses Interface**: Uses the `curses` library to display the document content and manage the text cursor.

## Server Implementation

### `RTFServiceServicer`

This class defines the gRPC service for document editing.

#### Methods

- **`InitializeClient(request, context)`**: Initializes the client with the current document content and change index.
- **`adjustPosition(client_last_change, change_position)`**: Adjusts the change position based on the client's last known change.
- **`handleInsert(request)`**: Handles insert operations and updates the document content.
- **`handleDelete(request)`**: Handles delete operations and updates the document content.
- **`SyncChanges(request, context)`**: Asynchronously sends document changes to the client.
- **`SendLocalChange(request, context)`**: Receives changes from a client and broadcasts them to all connected clients.

### Logging

The server uses Python's `logging` module to log events such as client connections, changes received, and broadcasts sent to clients.

## Running the Application

### Start the Server

To start the gRPC server, run the server script:

```bash
python server.py
```

### Start the Client

To start the client interface, run the client script:

```bash
python client.py
```

### To generate protos

From Q4 directory, run

```bash
sh protofiles/toBuild.sh
```

## Protobuf Definitions

The server and client communicate using the following Protobuf definitions:

# Document Protocol Buffers Definition

This document describes the Protocol Buffers (protobuf) definitions for the Real-Time Collaborative Document Editing application. It outlines the services, messages, and the data types used for communication between the client and server.

## Services

### `RTFService`

This service handles the core functionality of document editing.

#### RPC Methods

- **`InitializeClient(InitializeRequest) returns (DocumentContent)`**
  - Initializes a new client with the current document content.
  
- **`SyncChanges(stream SyncChange) returns (stream DocumentChange)`**
  - Synchronizes changes made by clients in real-time.

- **`SendLocalChange(DocumentChange) returns (AckMessage)`**
  - Sends a local change made by a client to the server for processing and broadcasting.

### `LoggingService`

This service is responsible for logging changes made to the document.

#### RPC Methods

- **`LogChanges(stream DocumentChange) returns (LogResponse)`**
  - Logs document changes for audit or debugging purposes.

## Messages

### `InitializeRequest`

- **`string client_id` (1)**: A unique identifier for the client.

### `SyncChange`

- **`string client_id` (1)**: The ID of the client who made the change.
- **`int32 changeIndex` (2)**: The index of the change, indicating the order in which changes were made.

### `DocumentContent`

- **`string content` (1)**: The current content of the document.
- **`int32 lastChange` (2)**: The last change number that was processed.

### `DocumentChange`

- **`string client_id` (1)**: The ID of the client who made the change.
- **`string change_type` (2)**: The type of change, either "insert" or "delete".
- **`int32 position` (3)**: The position in the document where the change occurred.
- **`string charChange` (4)**: The character inserted, or an empty string for deletion.
- **`int32 changeIndex` (5)**: The index of the change.

### `AckMessage`

- **`string message` (1)**: Acknowledgment message from the server.

### `LogResponse`

- **`string message` (1)**: Response message from the logging service.

## Implementation Quirks

1. **Client ID Management**: Each client must generate a unique client ID before connecting to the server. This ID is essential for tracking changes and synchronizing updates.

2. **Change Index Handling**: The `changeIndex` field is crucial for maintaining the order of changes. Clients must correctly manage this index to ensure that changes are applied in the correct sequence.

3. **Streaming RPCs**: The `SyncChanges` method uses streaming for both requests and responses, allowing for real-time updates. Clients must implement appropriate handling for continuous data streams.

4. **Error Handling**: While the protobuf definitions do not specify error messages, it's essential to implement robust error handling on both client and server sides to manage potential issues, such as network interruptions or invalid data.

5. **Logging Service**: The `LoggingService` is optional but can provide valuable insights into document changes for debugging or auditing purposes. Ensure that logging does not interfere with the real-time performance of the document editing.


