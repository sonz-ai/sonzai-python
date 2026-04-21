from enum import Enum

class ListSummariesPeriod(str, Enum):
    DAILY = "daily"
    VALUE_2 = ""
    WEEKLY = "weekly"

    def __str__(self) -> str:
        return str(self.value)
