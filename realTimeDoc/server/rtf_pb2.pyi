from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class InitializeRequest(_message.Message):
    __slots__ = ("client_id",)
    CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
    client_id: str
    def __init__(self, client_id: _Optional[str] = ...) -> None: ...

class SyncChange(_message.Message):
    __slots__ = ("client_id", "changeIndex")
    CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
    CHANGEINDEX_FIELD_NUMBER: _ClassVar[int]
    client_id: str
    changeIndex: int
    def __init__(self, client_id: _Optional[str] = ..., changeIndex: _Optional[int] = ...) -> None: ...

class DocumentContent(_message.Message):
    __slots__ = ("content", "lastChange")
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    LASTCHANGE_FIELD_NUMBER: _ClassVar[int]
    content: str
    lastChange: int
    def __init__(self, content: _Optional[str] = ..., lastChange: _Optional[int] = ...) -> None: ...

class DocumentChange(_message.Message):
    __slots__ = ("client_id", "change_type", "position", "charChange", "changeIndex")
    CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
    CHANGE_TYPE_FIELD_NUMBER: _ClassVar[int]
    POSITION_FIELD_NUMBER: _ClassVar[int]
    CHARCHANGE_FIELD_NUMBER: _ClassVar[int]
    CHANGEINDEX_FIELD_NUMBER: _ClassVar[int]
    client_id: str
    change_type: str
    position: int
    charChange: str
    changeIndex: int
    def __init__(self, client_id: _Optional[str] = ..., change_type: _Optional[str] = ..., position: _Optional[int] = ..., charChange: _Optional[str] = ..., changeIndex: _Optional[int] = ...) -> None: ...

class AckMessage(_message.Message):
    __slots__ = ("message",)
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: str
    def __init__(self, message: _Optional[str] = ...) -> None: ...

class LogResponse(_message.Message):
    __slots__ = ("message",)
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: str
    def __init__(self, message: _Optional[str] = ...) -> None: ...
