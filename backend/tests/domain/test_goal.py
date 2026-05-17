"""Tests for the Goal domain class."""

from datetime import date, time, timedelta
from uuid import uuid4

import pytest
from pydantic import ValidationError

from app.domain.enums import ConfidenceLevel, GoalStatus, LearningStyle
from app.domain.goal import Goal


# ---------------------------------------------------------------------------
# Fixture
# ---------------------------------------------------------------------------

@pytest.fixture
def valid_goal_data() -> dict:
    return {
        "user_id": uuid4(),
        "title": "Pass CKA exam",
        "deadline_date": date.today() + timedelta(days=90),
        "daily_available_minutes": 60,
        "confidence_level": ConfidenceLevel.LOW,
        "learning_style": LearningStyle.PRACTICE,
    }


# ---------------------------------------------------------------------------
# Happy path
# ---------------------------------------------------------------------------

def test_goal_creates_with_valid_data(valid_goal_data):
    goal = Goal(**valid_goal_data)

    assert goal.title == "Pass CKA exam"
    assert goal.status == GoalStatus.ACTIVE   # default value
    assert goal.description is None           # optional field defaults to None
    assert goal.id is not None


def test_goal_accepts_optional_fields(valid_goal_data):
    valid_goal_data["description"] = "Certified Kubernetes Administrator"
    valid_goal_data["preferred_study_time"] = time(7, 0)

    goal = Goal(**valid_goal_data)

    assert goal.description == "Certified Kubernetes Administrator"
    assert goal.preferred_study_time == time(7, 0)


def test_goal_accepts_all_confidence_levels(valid_goal_data):
    for level in ConfidenceLevel:
        valid_goal_data["confidence_level"] = level
        goal = Goal(**valid_goal_data)
        assert goal.confidence_level == level


def test_goal_accepts_all_learning_styles(valid_goal_data):
    for style in LearningStyle:
        valid_goal_data["learning_style"] = style
        goal = Goal(**valid_goal_data)
        assert goal.learning_style == style


def test_goal_accepts_string_enum_values(valid_goal_data):
    """Pydantic coerces plain strings into enum members automatically."""
    valid_goal_data["confidence_level"] = "HIGH"
    valid_goal_data["learning_style"] = "READING"

    goal = Goal(**valid_goal_data)

    assert goal.confidence_level == ConfidenceLevel.HIGH
    assert goal.learning_style == LearningStyle.READING


# ---------------------------------------------------------------------------
# Title validation
# ---------------------------------------------------------------------------

def test_goal_rejects_empty_title(valid_goal_data):
    valid_goal_data["title"] = ""

    with pytest.raises(ValidationError) as exc_info:
        Goal(**valid_goal_data)

    errors = exc_info.value.errors()
    assert any(e["loc"] == ("title",) for e in errors)


def test_goal_rejects_whitespace_only_title(valid_goal_data):
    valid_goal_data["title"] = "   "

    with pytest.raises(ValidationError):
        Goal(**valid_goal_data)


def test_goal_strips_whitespace_from_title(valid_goal_data):
    valid_goal_data["title"] = "  Pass CKA exam  "
    goal = Goal(**valid_goal_data)

    assert goal.title == "Pass CKA exam"


def test_goal_rejects_title_exceeding_max_length(valid_goal_data):
    valid_goal_data["title"] = "A" * 256

    with pytest.raises(ValidationError):
        Goal(**valid_goal_data)


# ---------------------------------------------------------------------------
# Deadline validation
# ---------------------------------------------------------------------------

def test_goal_rejects_past_deadline(valid_goal_data):
    valid_goal_data["deadline_date"] = date.today() - timedelta(days=1)

    with pytest.raises(ValidationError) as exc_info:
        Goal(**valid_goal_data)

    # model_validator errors appear under the root key
    errors = exc_info.value.errors()
    assert any("deadline" in str(e["msg"]).lower() for e in errors)


def test_goal_rejects_deadline_today(valid_goal_data):
    valid_goal_data["deadline_date"] = date.today()

    with pytest.raises(ValidationError):
        Goal(**valid_goal_data)


def test_goal_accepts_deadline_tomorrow(valid_goal_data):
    valid_goal_data["deadline_date"] = date.today() + timedelta(days=1)
    goal = Goal(**valid_goal_data)

    assert goal.deadline_date == date.today() + timedelta(days=1)


# ---------------------------------------------------------------------------
# Daily available minutes validation
# ---------------------------------------------------------------------------

def test_goal_rejects_minutes_below_minimum(valid_goal_data):
    valid_goal_data["daily_available_minutes"] = 4   # min is 5

    with pytest.raises(ValidationError):
        Goal(**valid_goal_data)


def test_goal_rejects_minutes_above_maximum(valid_goal_data):
    valid_goal_data["daily_available_minutes"] = 481  # max is 480

    with pytest.raises(ValidationError):
        Goal(**valid_goal_data)


def test_goal_accepts_boundary_minutes(valid_goal_data):
    valid_goal_data["daily_available_minutes"] = 5
    assert Goal(**valid_goal_data).daily_available_minutes == 5

    valid_goal_data["daily_available_minutes"] = 480
    assert Goal(**valid_goal_data).daily_available_minutes == 480


# ---------------------------------------------------------------------------
# Enum validation
# ---------------------------------------------------------------------------

def test_goal_rejects_invalid_confidence_level(valid_goal_data):
    valid_goal_data["confidence_level"] = "VERY_HIGH"

    with pytest.raises(ValidationError):
        Goal(**valid_goal_data)


def test_goal_rejects_invalid_learning_style(valid_goal_data):
    valid_goal_data["learning_style"] = "KINESTHETIC"

    with pytest.raises(ValidationError):
        Goal(**valid_goal_data)
