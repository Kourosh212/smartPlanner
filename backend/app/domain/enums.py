from enum import Enum


# (str, Enum) makes values behave like plain strings — equivalent to
# StrEnum (Python 3.11+) but compatible with Python 3.10.
# Java analogy: enum GoalStatus { ACTIVE, COMPLETED, ABANDONED }
class GoalStatus(str, Enum):
    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"
    ABANDONED = "ABANDONED"


class ConfidenceLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class LearningStyle(str, Enum):
    READING = "READING"
    PRACTICE = "PRACTICE"
    VISUAL = "VISUAL"
    AUDIO = "AUDIO"
