# Relational Database Diagram — Adaptive Interview Habit Coach

```mermaid
erDiagram
    users {
        uuid id PK
        varchar email UK
        varchar name
        varchar password_hash
        timestamp created_at
        timestamp updated_at
    }

    goals {
        uuid id PK
        uuid user_id FK
        varchar title
        text description
        date deadline_date
        int daily_available_minutes
        time preferred_study_time
        varchar confidence_level
        varchar learning_style
        varchar status
        timestamp created_at
        timestamp updated_at
    }

    planning_profiles {
        uuid id PK
        uuid user_id FK
        time preferred_study_time
        int best_session_length_minutes
        varchar common_missed_reason
        varchar habit_level
        timestamp updated_at
    }

    planning_profile_weak_topics {
        uuid id PK
        uuid planning_profile_id FK
        varchar topic
    }

    planning_profile_avoid_days {
        uuid id PK
        uuid planning_profile_id FK
        varchar day_of_week
    }

    journeys {
        uuid id PK
        uuid goal_id FK
        varchar title
        int week_number
        text description
        varchar status
        date start_date
        date end_date
    }

    habits {
        uuid id PK
        uuid goal_id FK
        uuid journey_id FK
        varchar title
        text description
        int duration_minutes
        varchar topic
        int order_index
        timestamp created_at
    }

    daily_plans {
        uuid id PK
        uuid user_id FK
        uuid goal_id FK
        date plan_date
        timestamp created_at
    }

    tasks {
        uuid id PK
        uuid daily_plan_id FK
        uuid habit_id FK
        varchar type
        varchar title
        text description
        int duration_minutes
        varchar status
        timestamp completed_at
        timestamp created_at
    }

    missed_task_logs {
        uuid id PK
        uuid task_id FK
        varchar reason
        text custom_reason
        timestamp logged_at
    }

    reflections {
        uuid id PK
        uuid task_id FK
        varchar difficulty_rating
        int confidence_level
        boolean wants_more_practice
        text notes
        timestamp created_at
    }

    notifications {
        uuid id PK
        uuid user_id FK
        uuid task_id FK
        varchar type
        text message
        timestamp scheduled_at
        timestamp sent_at
        varchar status
    }

    llm_reasoning_logs {
        uuid id PK
        uuid user_id FK
        uuid goal_id FK
        uuid task_id FK
        text prompt_summary
        varchar recommended_action
        decimal confidence
        jsonb raw_response
        boolean applied
        timestamp created_at
    }

    users ||--o{ goals : "creates"
    users ||--|| planning_profiles : "has one"
    users ||--o{ daily_plans : "receives"
    users ||--o{ notifications : "receives"
    users ||--o{ llm_reasoning_logs : "generates"

    goals ||--o{ journeys : "structured into"
    goals ||--o{ habits : "broken into"
    goals ||--o{ daily_plans : "drives"
    goals ||--o{ llm_reasoning_logs : "referenced in"

    planning_profiles ||--o{ planning_profile_weak_topics : "tracks"
    planning_profiles ||--o{ planning_profile_avoid_days : "avoids"

    journeys ||--o{ habits : "contains"

    daily_plans ||--o{ tasks : "includes"

    habits ||--o{ tasks : "instantiated as"

    tasks ||--o| missed_task_logs : "logged when missed"
    tasks ||--o| reflections : "followed by"
    tasks ||--o{ notifications : "triggers"
    tasks ||--o{ llm_reasoning_logs : "informs"
```

---

## Entity Reference

| Entity | Purpose |
|---|---|
| `users` | Core account. All data is scoped to a user. |
| `goals` | High-level objective with deadline, daily time, confidence level, and learning style collected at onboarding. |
| `planning_profiles` | One per user. Learned behavioural patterns used by the adaptive coach (preferred time, habit level, common missed reason). |
| `planning_profile_weak_topics` | Normalised list of topics the user struggles with (e.g. `etcd`, `scheduler`). |
| `planning_profile_avoid_days` | Days the coach should avoid scheduling heavy tasks (e.g. `Friday`). |
| `journeys` | Phased weekly sequence tied to a goal (e.g. "Week 2: Strengthen fundamentals"). |
| `habits` | Template-level small repeatable actions generated from a goal inside a journey. |
| `daily_plans` | One plan per user per goal per day. Groups the day's tasks. |
| `tasks` | Concrete scheduled instance of a habit. Holds the live status. |
| `missed_task_logs` | One-to-one with a missed task. Captures the reason for adaptive rescheduling. |
| `reflections` | Post-task self-assessment (difficulty, confidence, wants more practice). Feeds future planning. |
| `notifications` | Scheduled or sent messages. Non-guilt-based, tied to tasks or user context. |
| `llm_reasoning_logs` | Audit trail for every LLM call. `applied` tracks whether the backend accepted the recommendation. |

---

## Key Enums

| Field | Values |
|---|---|
| `goals.status` | `ACTIVE`, `COMPLETED`, `ABANDONED` |
| `goals.confidence_level` | `LOW`, `MEDIUM`, `HIGH` |
| `goals.learning_style` | `READING`, `PRACTICE`, `VISUAL`, `AUDIO` |
| `journeys.status` | `PENDING`, `IN_PROGRESS`, `COMPLETED` |
| `tasks.type` | `MAIN_HABIT`, `STRETCH_TASK`, `REFLECTION` |
| `tasks.status` | `PENDING`, `COMPLETED`, `MISSED`, `RESCHEDULED`, `SKIPPED` |
| `missed_task_logs.reason` | `TOO_BUSY`, `TOO_TIRED`, `FORGOT`, `TOO_HARD`, `TOO_LONG`, `NOT_MOTIVATED`, `PERSONAL_ISSUE`, `TOPIC_UNCLEAR`, `CUSTOM` |
| `reflections.difficulty_rating` | `TOO_EASY`, `RIGHT_LEVEL`, `TOO_HARD` |
| `notifications.type` | `HABIT_REMINDER`, `MISSED_FOLLOWUP`, `MOTIVATIONAL`, `SCHEDULE_ADJUSTMENT` |
| `notifications.status` | `PENDING`, `SENT`, `FAILED` |
| `planning_profiles.habit_level` | `STARTER`, `INTERMEDIATE`, `ADVANCED` |
