import curses
import grpc
import rtf_pb2, rtf_pb2_grpc
import threading
import asyncio
import random

class DocumentClient:
    def __init__(self):
        self.client_id = str(random.randint(1, 1000))
        self.document_content = ['']
        self.last_change = 0
        self.stub = None

    async def sync_changes(self):
        try:
            async for change in self.stub.SyncChanges(rtf_pb2.SyncChange(client_id=self.client_id, changeIndex=self.last_change)):
                try:
                    if change.change_type == 'insert':
                        self.document_content = (
                            self.document_content[:change.position] + 
                            change.charChange + 
                            self.document_content[change.position:]
                        )
                        self.last_change = change.changeIndex
                    elif change.change_type == 'delete':
                        self.document_content = (
                            self.document_content[:change.position] + 
                            self.document_content[change.position + 1:]
                        )
                        self.last_change = change.changeIndex
                except Exception as e:
                    print(f"Error processing change: {e}")
        except grpc.aio.AioRpcError as e:
            print(f"gRPC sync error: {e}")
        except Exception as e:
            print(f"General sync error: {e}")

    async def send_changes(self, change_type, char_change, position):
        try:
            changeReq = rtf_pb2.DocumentChange(
                client_id=self.client_id,
                change_type=change_type,
                position=position,
                charChange=char_change,
                changeIndex=self.last_change
            )
            response = await self.stub.SendLocalChange(changeReq)
        except grpc.aio.AioRpcError as e:
            print(f"gRPC send error: {e}")
        except Exception as e:
            print(f"Error sending local change: {e}")

    async def initialize_document(self):
        try:
            initializeReq = rtf_pb2.InitializeRequest(client_id=self.client_id)
            response = await self.stub.InitializeClient(initializeReq)
            self.document_content = response.content.splitlines()
            self.last_change = response.lastChange
        except grpc.aio.AioRpcError as e:
            print(f"gRPC initialize error: {e}")
        except Exception as e:
            print(f"Error initializing document: {e}")

    async def run(self, stdscr):
        try:
            async with grpc.aio.insecure_channel('localhost:50051') as channel:
                self.stub = rtf_pb2_grpc.RTFServiceStub(channel)
                await self.initialize_document()
                
                # Initialize the cursor position
                cursor_x, cursor_y = 0, 0
                curses.curs_set(1)

                # Start the change synchronization in a separate thread
                threading.Thread(target=asyncio.run, args=(self.sync_changes(),), daemon=True).start()

                while True:
                    stdscr.clear()
                    for y, line in enumerate(self.document_content):
                        stdscr.addstr(y, 0, line)
                    stdscr.move(cursor_y, cursor_x)
                    stdscr.refresh()

                    key = stdscr.getch()

                    if key == 27:  # ESC key
                        break
                    elif key in (curses.KEY_BACKSPACE, 8, 127):
                        if cursor_x > 0:
                            cursor_x -= 1
                            deleted_char = self.document_content[cursor_y][cursor_x]
                            self.document_content[cursor_y] = (
                                self.document_content[cursor_y][:cursor_x] + 
                                self.document_content[cursor_y][cursor_x + 1:]
                            )
                            await self.send_changes('delete', deleted_char, cursor_x)
                        elif cursor_y > 0:
                            cursor_y -= 1
                            cursor_x = len(self.document_content[cursor_y])
                            deleted_char = self.document_content[cursor_y][-1] if self.document_content[cursor_y] else ''
                            if deleted_char:
                                self.document_content[cursor_y] = self.document_content[cursor_y][:-1]
                                await self.send_changes('delete', deleted_char, cursor_x)
                    elif key == curses.KEY_ENTER or key == 10:
                        current_line = self.document_content[cursor_y]
                        new_line = current_line[cursor_x:]
                        self.document_content[cursor_y] = current_line[:cursor_x]
                        cursor_y += 1
                        self.document_content.insert(cursor_y, new_line)
                        cursor_x = 0
                        await self.send_changes('newline', '', cursor_x)
                    elif key == curses.KEY_LEFT:
                        if cursor_x > 0:
                            cursor_x -= 1
                        elif cursor_y > 0:
                            cursor_y -= 1
                            cursor_x = len(self.document_content[cursor_y])
                    elif key == curses.KEY_RIGHT:
                        if cursor_x < len(self.document_content[cursor_y]):
                            cursor_x += 1
                        elif cursor_y < len(self.document_content) - 1:
                            cursor_y += 1
                            cursor_x = 0
                    elif key == curses.KEY_UP:
                        if cursor_y > 0:
                            cursor_y -= 1
                    elif key == curses.KEY_DOWN:
                        if cursor_y < len(self.document_content) - 1:
                            cursor_y += 1
                            cursor_x = min(cursor_x, len(self.document_content[cursor_y]))
                    elif 32 <= key <= 126:  # Handle printable characters
                        if cursor_y >= len(self.document_content):
                            self.document_content.append('')
                        self.document_content[cursor_y] = (
                            self.document_content[cursor_y][:cursor_x] + 
                            chr(key) + 
                            self.document_content[cursor_y][cursor_x:]
                        )
                        cursor_x += 1
                        await self.send_changes('insert', chr(key), cursor_x - 1)

        except Exception as e:
            print(f"Error in run: {e}")

# Wrapper function to run the asyncio event loop
def main(stdscr):
    client = DocumentClient()
    asyncio.run(client.run(stdscr))

if __name__ == "__main__":
    curses.wrapper(main)
