"""
Tests for the User domain class.

Java analogy:
  - Each function starting with test_ = a @Test method in JUnit 5
  - pytest.raises(...)  = assertThrows(...) in JUnit 5
  - plain `assert`      = assertEquals / assertTrue / assertNotNull
  - @pytest.fixture     = @BeforeEach setup shared across tests
"""

import pytest
from pydantic import ValidationError

from app.domain.user import User


# ---------------------------------------------------------------------------
# Fixture — Java equivalent: @BeforeEach or a helper factory method
# ---------------------------------------------------------------------------

@pytest.fixture
def valid_user_data() -> dict:
    """Minimal valid payload to construct a User."""
    return {
        "email": "alice@example.com",
        "name": "Alice",
        "password_hash": "$2b$12$hashed_password_value",
    }


# ---------------------------------------------------------------------------
# Happy path
# ---------------------------------------------------------------------------

def test_user_creates_with_valid_data(valid_user_data):
    user = User(**valid_user_data)

    assert user.email == "alice@example.com"
    assert user.name == "Alice"
    assert user.id is not None          # UUID auto-generated
    assert user.created_at is not None
    assert user.updated_at is not None


def test_user_generates_unique_ids(valid_user_data):
    user1 = User(**valid_user_data)
    user2 = User(**valid_user_data)

    assert user1.id != user2.id


def test_user_is_immutable(valid_user_data):
    """frozen=True means no field can be changed after construction."""
    user = User(**valid_user_data)

    # Java analogy: trying to set a final field — should throw
    with pytest.raises(Exception):
        user.name = "Bob"  # type: ignore[misc]


# ---------------------------------------------------------------------------
# Email validation
# ---------------------------------------------------------------------------

def test_user_rejects_invalid_email(valid_user_data):
    valid_user_data["email"] = "not-an-email"

    with pytest.raises(ValidationError) as exc_info:
        User(**valid_user_data)

    # ValidationError carries a list of errors — check we caught the right one
    errors = exc_info.value.errors()
    assert any(e["loc"] == ("email",) for e in errors)


def test_user_rejects_missing_email(valid_user_data):
    del valid_user_data["email"]

    with pytest.raises(ValidationError):
        User(**valid_user_data)


# ---------------------------------------------------------------------------
# Name validation
# ---------------------------------------------------------------------------

def test_user_rejects_empty_name(valid_user_data):
    valid_user_data["name"] = ""

    with pytest.raises(ValidationError) as exc_info:
        User(**valid_user_data)

    errors = exc_info.value.errors()
    assert any(e["loc"] == ("name",) for e in errors)


def test_user_rejects_whitespace_only_name(valid_user_data):
    valid_user_data["name"] = "   "

    with pytest.raises(ValidationError):
        User(**valid_user_data)


def test_user_strips_whitespace_from_name(valid_user_data):
    valid_user_data["name"] = "  Alice  "
    user = User(**valid_user_data)

    assert user.name == "Alice"


def test_user_rejects_name_exceeding_max_length(valid_user_data):
    valid_user_data["name"] = "A" * 101

    with pytest.raises(ValidationError):
        User(**valid_user_data)


# ---------------------------------------------------------------------------
# Password hash validation
# ---------------------------------------------------------------------------

def test_user_rejects_empty_password_hash(valid_user_data):
    valid_user_data["password_hash"] = ""

    with pytest.raises(ValidationError):
        User(**valid_user_data)
