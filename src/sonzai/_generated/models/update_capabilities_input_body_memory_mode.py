from enum import Enum

class UpdateCapabilitiesInputBodyMemoryMode(str, Enum):
    ASYNC = "async"
    SYNC = "sync"

    def __str__(self) -> str:
        return str(self.value)
