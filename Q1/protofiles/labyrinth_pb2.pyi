from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Empty(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class LabyrinthInfo(_message.Message):
    __slots__ = ("width", "height")
    WIDTH_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    width: int
    height: int
    def __init__(self, width: _Optional[int] = ..., height: _Optional[int] = ...) -> None: ...

class PlayerStatus(_message.Message):
    __slots__ = ("x", "y", "hp", "rem_spells", "score")
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    HP_FIELD_NUMBER: _ClassVar[int]
    REM_SPELLS_FIELD_NUMBER: _ClassVar[int]
    SCORE_FIELD_NUMBER: _ClassVar[int]
    x: int
    y: int
    hp: int
    rem_spells: int
    score: int
    def __init__(self, x: _Optional[int] = ..., y: _Optional[int] = ..., hp: _Optional[int] = ..., rem_spells: _Optional[int] = ..., score: _Optional[int] = ...) -> None: ...

class MoveRequest(_message.Message):
    __slots__ = ("direction",)
    DIRECTION_FIELD_NUMBER: _ClassVar[int]
    direction: str
    def __init__(self, direction: _Optional[str] = ...) -> None: ...

class MoveResponse(_message.Message):
    __slots__ = ("status",)
    STATUS_FIELD_NUMBER: _ClassVar[int]
    status: int
    def __init__(self, status: _Optional[int] = ...) -> None: ...

class TilePosition(_message.Message):
    __slots__ = ("x", "y")
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    x: int
    y: int
    def __init__(self, x: _Optional[int] = ..., y: _Optional[int] = ...) -> None: ...

class TargetPosition(_message.Message):
    __slots__ = ("x", "y")
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    x: int
    y: int
    def __init__(self, x: _Optional[int] = ..., y: _Optional[int] = ...) -> None: ...

class RevelioRequest(_message.Message):
    __slots__ = ("x", "y", "tile_type")
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    TILE_TYPE_FIELD_NUMBER: _ClassVar[int]
    x: int
    y: int
    tile_type: int
    def __init__(self, x: _Optional[int] = ..., y: _Optional[int] = ..., tile_type: _Optional[int] = ...) -> None: ...

class BombardaResponse(_message.Message):
    __slots__ = ("status",)
    STATUS_FIELD_NUMBER: _ClassVar[int]
    status: str
    def __init__(self, status: _Optional[str] = ...) -> None: ...

class Grid(_message.Message):
    __slots__ = ("gridrow",)
    GRIDROW_FIELD_NUMBER: _ClassVar[int]
    gridrow: _containers.RepeatedCompositeFieldContainer[GridRow]
    def __init__(self, gridrow: _Optional[_Iterable[_Union[GridRow, _Mapping]]] = ...) -> None: ...

class GridRow(_message.Message):
    __slots__ = ("val",)
    VAL_FIELD_NUMBER: _ClassVar[int]
    val: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, val: _Optional[_Iterable[str]] = ...) -> None: ...
