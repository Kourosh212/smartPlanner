# Software Requirements Specification (SRS)
## Project: Adaptive Interview Habit Coach

---

## 1. Purpose

The purpose of this application is to help users prepare for interviews, exams, and technical learning goals by turning large goals into **small daily habits**.

The system should not behave like a simple task tracker. It should behave like a **personal adaptive coach** that:

- starts with small achievable habits
- tracks consistency
- asks why tasks were missed
- adjusts the next plan based on user behaviour
- uses LLM reasoning safely and in a controlled way

---

## 2. Product Vision

The app should follow a **habit-building UX**:

- beautiful and calming interface
- small daily commitments bases on the initail requirment of user
- habit streaks
- motivational but practical guidance
- progressive journeys
- gentle recovery after missed tasks
- no guilt-based messaging

The main initial use case is:

> Helping a user prepare for an interview or exam through small, consistent learning habits.

Example:

> “Prepare for Kubernetes interview in 30 days” becomes:
> “Today: 15 minutes : explain Pod lifecycle in your own words.”

---

## 3. Platform Requirement

### 3.1 Mobile Application

The frontend must be a **real React Native mobile application**.

Supported platforms:

- Android
- iOS

The application must be publishable to:

- Google Play Store
- Apple App Store

### 3.2 Not In Scope

The MVP must not be implemented as:

- React web app only
- PWA only
- native Android-only app
- native iOS-only app

---

## 4. High-Level Architecture

```text
React Native Mobile App
        ↓
Spring Boot Backend API
        ↓
PostgreSQL Database
        ↓
LLM API
        ↓
Notification Service
```

---

## 5. Core Product Concepts

### 5.1 Goal

A high-level user objective.

Examples:

- Prepare for Java concurrency interview
- Prepare for system design interview
- Prepare for algorithm leetcode.com

### 5.2 Habit

A small repeatable action that supports the goal.

Examples:

- Study for 15 minutes
- Answer one interview question
- Review one weak topic
- Explain one concept aloud

### 5.3 Journey

A guided sequence of habits and learning tasks.

Example:

```text
Week 1: Build consistency
Week 2: Strengthen fundamentals
Week 3: Practice interview scenarios
Week 4: Mock interview and review
```

### 5.4 Adaptive Coach

The reasoning layer that adjusts plans based on:

- missed tasks
- task difficulty
- user energy
- available time
- repeated behaviour patterns
- learning weaknesses

---

## 6. Functional Requirements

---

## 6.1 User Onboarding

The app shall collect:

- target goal
- deadline or target date
- daily available time
- preferred study time
- current confidence level
- preferred learning style

Example onboarding question:

> “How much time can you realistically give each day?”

Options:

- 5 minutes
- 15 minutes
- 30 minutes
- 45 minutes
- 60 minutes

> Then LLM suggest based on your goal you need X minutes to commit. Can you find more time? 
---

## 6.2 Small Habit Creation

The system shall break large goals into small habits.

Example:

Instead of:

> Study Kubernetes

The system creates:

> Spend 15 minutes explaining how a Pod is scheduled.

The first tasks must be intentionally small to build consistency.

---

## 6.3 Daily Plan

Each day, the user receives a small daily plan.

A daily plan may include:

- one main learning habit
- one optional stretch task
- one reflection question

Example:

```text
Main habit:
Answer one Kubernetes interview question.

Stretch task:
Read about etcd quorum for 10 minutes.

Reflection:
Was this too easy, too hard, or right level?
```

---

## 6.4 Task States

Each task shall support these states:

- PENDING
- COMPLETED
- MISSED
- RESCHEDULED
- SKIPPED

---

## 6.5 Missed Task Reason Capture

If the user misses a task, the app must ask for the reason.

Predefined reasons:

- Too busy
- Too tired
- Forgot
- Task was too hard
- Task was too long
- Not motivated
- Unexpected personal issue
- Topic was unclear

The user can also provide a custom reason.

---

## 6.6 Adaptive Rescheduling

The system shall adjust future plans based on the missed reason.

Examples:

| Missed Reason | System Behaviour |
|---|---|
| Too busy | Reduce next task duration |
| Too tired | Schedule lighter task |
| Forgot | Improve reminder timing |
| Too hard | Break topic into smaller prerequisite tasks |
| Too long | Split task into smaller sessions |
| Not motivated | Provide easier restart task |

---

## 6.7 Planning Profile

The system shall maintain a planning profile for each user.

The planning profile stores learned patterns such as:

```json
{
  "preferredStudyTime": "20:00",
  "bestSessionLengthMinutes": 15,
  "commonMissedReason": "too_tired",
  "weakTopics": ["etcd", "scheduler"],
  "avoidHeavyTasksOn": ["Friday"],
  "habitLevel": "starter"
}
```

This profile must be stored in the database, not inside the LLM.

---

## 6.8 Progress Tracking

The app shall show:

- habit streak
- completed tasks
- missed tasks
- weak topics
- confidence trend
- current journey stage

The progress view should be simple and motivational, not overloaded with charts.

---

## 6.9 Notifications

The app shall support smart notifications.

Notification examples:

- “Your 15-minute interview habit is ready.”
- “Yesterday was missed. Want to restart with a 5-minute version?”
- “You usually do better after 8 PM. Shall we keep today’s session light?”

Notifications must be supportive and non-guilt-based.

---

## 6.10 Reflection

After a task, the app should ask a short reflection question.

Examples:

- Was this task too easy, right level, or too hard?
- How confident do you feel about this topic?
- Do you want more practice on this topic?

Reflection data must influence future planning.

---

## 7. Reasoning Best Practices

The LLM must not be treated as the system of record.

### 7.1 Source of Truth

The database is the source of truth for:

- goals
- habits
- task status
- missed reasons
- user reflections
- planning profile
- progress history

The LLM is used only for reasoning and generation.

---

### 7.2 Controlled Reasoning

The backend must control the workflow.

The LLM may suggest:

- plan adjustments
- smaller task breakdowns
- motivational messages
- interview questions
- feedback

The backend must validate and approve the final action.

---

### 7.3 Structured LLM Output

All LLM responses used by the backend must be returned in strict JSON format.

Example:

```json
{
  "recommendedAction": "REDUCE_TASK_SIZE",
  "reason": "User missed task due to lack of time",
  "nextTaskDurationMinutes": 10,
  "confidence": 0.82
}
```

---

### 7.4 No Blind Autonomy

The LLM must not directly:

- update the database
- send notifications
- modify schedules
- make final workflow decisions

It must return recommendations only.

---

### 7.5 Explainable Planning

When the plan changes, the app should explain why.

Example:

> “We reduced today’s task to 10 minutes because you missed two 30-minute sessions this week.”

---

### 7.6 Habit-Safe Reasoning

The system must prefer consistency over intensity.

Example rule:

> If the user repeatedly misses 45-minute tasks, reduce to 10–15 minutes rather than pushing harder.

---

## 8. Backend Requirements

Backend technology:

- Java 21
- Spring Boot
- PostgreSQL
- REST APIs
- LLM API integration

Backend responsibilities:

- user management
- goal management
- habit generation
- plan tracking
- reasoning orchestration
- notification triggering
- persistence
- audit trail

---

## 9. Mobile App Requirements

Technology:

- React Native
- TypeScript preferred

The mobile app shall include:

- onboarding screens
- goal setup
- daily habit screen
- missed reason screen
- progress screen
- reflection screen
- notification handling

The app should follow a polished, calming habit-coach style inspired by Fabulous.

---

## 10. MVP Scope

MVP must include:

1. React Native mobile app
2. Goal creation
3. Small habit generation
4. Daily habit tracking
5. Missed reason capture
6. Adaptive rescheduling
7. Planning profile
8. Basic progress screen
9. Smart notifications
10. LLM reasoning with strict backend control

---

## 11. Out of Scope for MVP

The following are not required for MVP:

- voice interaction
- full mock interview mode
- social features
- complex gamification
- payment/subscription system
- vector database
- advanced analytics dashboard

---

## 12. Acceptance Criteria

The MVP is accepted when:

- user can create an interview or study goal
- system generates small daily habits
- user can complete or miss a task
- missed task requires reason capture
- system adjusts future tasks based on reason
- planning profile is updated
- progress is visible in the app
- notifications are supported
- LLM output is structured and validated
- database remains the source of truth

---

## 13. Product Principle

> The system should help users recover from failed plans, not make them feel guilty for failing.

The main objective is to create sustainable learning behaviour through small habits, adaptive planning, and controlled AI reasoning.