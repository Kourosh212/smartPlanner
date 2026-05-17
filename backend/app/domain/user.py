from datetime import datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class User(BaseModel):
    """
    Core user account. All data in the system is scoped to a user.

    Java analogy: this is your @Entity class, but validation is built-in
    via Pydantic — no separate @Valid / Bean Validation annotations needed.
    """

    # ConfigDict(frozen=True) makes this immutable after construction,
    # like a Java record or a class with only final fields.
    model_config = ConfigDict(frozen=True)

    # uuid4() generates a new UUID by default — equivalent to
    # @GeneratedValue(strategy = GenerationType.UUID) in JPA.
    id: UUID = Field(default_factory=uuid4)

    # EmailStr validates format automatically — like @Email in Bean Validation.
    email: EmailStr = Field(
        description="Unique email address used for login",
    )

    name: str = Field(
        min_length=1,
        max_length=100,
        description="Display name shown in the UI",
    )

    # Stored as a bcrypt hash — never the raw password.
    password_hash: str = Field(
        min_length=1,
        description="bcrypt hash of the user password",
    )

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # @field_validator is the Pydantic v2 equivalent of a custom
    # @AssertTrue / ConstraintValidator in Java Bean Validation.
    @field_validator("name")
    @classmethod
    def name_must_not_be_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("name must not be blank or whitespace only")
        return value.strip()
