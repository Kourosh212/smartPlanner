from datetime import date, datetime, time
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from app.domain.enums import ConfidenceLevel, GoalStatus, LearningStyle


class Goal(BaseModel):
    """
    High-level objective a user wants to achieve.

    Carries the onboarding snapshot: deadline, daily capacity,
    confidence level, and preferred learning style.
    """

    model_config = ConfigDict(frozen=True)

    id: UUID = Field(default_factory=uuid4)

    # FK relationship — stored as UUID, resolved by the repository layer later.
    # Java analogy: @ManyToOne without the ORM join here; domain stays pure.
    user_id: UUID

    title: str = Field(
        min_length=1,
        max_length=255,
        description="Short, human-readable name of the goal",
    )

    # Optional[str] in Python == Optional<String> in Java.
    # "= None" means the field has a default of None (nullable).
    description: str | None = Field(
        default=None,
        max_length=2000,
        description="Longer explanation of what the user wants to achieve",
    )

    deadline_date: date = Field(
        description="Target date by which the goal should be completed",
    )

    # ge = greater-than-or-equal (like @Min in Bean Validation)
    # le = less-than-or-equal  (like @Max)
    daily_available_minutes: int = Field(
        ge=5,
        le=480,
        description="How many minutes per day the user can dedicate (5–480)",
    )

    preferred_study_time: time | None = Field(
        default=None,
        description="Time of day the user prefers to study, e.g. 07:00",
    )

    # StrEnum values are accepted as plain strings too, so "LOW" and
    # ConfidenceLevel.LOW are both valid — Pydantic coerces automatically.
    confidence_level: ConfidenceLevel = Field(
        description="User's self-assessed confidence before starting",
    )

    learning_style: LearningStyle = Field(
        description="Preferred way the user absorbs new material",
    )

    status: GoalStatus = Field(
        default=GoalStatus.ACTIVE,
        description="Lifecycle status of the goal",
    )

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    @field_validator("title")
    @classmethod
    def title_must_not_be_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("title must not be blank or whitespace only")
        return value.strip()

    # @model_validator runs after all fields are populated — like a class-level
    # @AssertTrue or a custom Validator in Java that needs multiple fields.
    @model_validator(mode="after")
    def deadline_must_be_in_the_future(self) -> "Goal":
        if self.deadline_date <= date.today():
            raise ValueError("deadline_date must be a future date")
        return self
