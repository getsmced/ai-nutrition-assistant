# AI Nutrition Assistant — Handoff

Use this file to resume the project in a fresh chat or task.

## Collaboration Rule

The user writes implementation code manually.

The assistant may:

- explain code step by step,
- review snippets or screenshots,
- suggest what the user should type,
- update documentation files in `docs/` to record progress.

The assistant must not modify real code files, migrations, frontend files, backend files, infrastructure files, or dependency files.

## Current Goal

Build an AI-powered nutrition planning application with a guarded multi-agent architecture.

The system should use:

- structured user profile data,
- deterministic Python calculations,
- explicit validation rules,
- curated evidence/guideline notes,
- agents for conversation, planning, explanation, and meal alternatives.

The LLM must not be the final authority for calories, macros, allergies, unsafe goals, or medical safety boundaries.

## Current Code Area

We are working through:

```text
backend/app/models.py
```

The current focus is adding the first MVP `NutritionProfile` model manually.

## What Has Been Explained

The user has learned/reviewed:

- imports in `models.py`, including `SQLModel`, `Field`, and `Relationship`,
- why `Literal` comes from `typing`, not from `sqlmodel`,
- the difference between API schemas and database models,
- `UserBase`, `UserCreate`, `UserRegister`, `UserUpdate`, `User`, `UserPublic`, and `UsersPublic`,
- why `password` is accepted as input but only `hashed_password` is stored,
- how `crud.py` uses `get_password_hash(...)` and passes the value into `User.hashed_password`,
- what `table=True` means,
- what `primary_key=True` means,
- how `Relationship(back_populates=...)` works,
- why strings are used inside `back_populates`,
- why stable English backend keys should map to Greek UI labels.

## Current MVP Model Decisions

Use these type aliases outside classes in `models.py`:

```python
Sex = Literal["male", "female"]
NutritionGoal = Literal["fat_loss", "muscle_gain", "maintenance"]
GoalIntensity = Literal["mild", "moderate", "intense"]
ActivityLevel = Literal["sedentary", "light", "moderate", "very_active"]
```

Do not add these aliases for MVP:

```text
DietaryPattern
Allergen
ExerciseType
CookingSkill
BudgetLevel
```

Reason:

- dietary patterns are not part of the current MVP,
- allergies are free-text `list[str]`,
- exercise stays simple,
- cooking skill and budget are postponed,
- food choices belong in a future food catalog, not in `models.py` Literals.

## Current `NutritionProfileBase` Shape

The user started writing this manually:

```python
class NutritionProfileBase(SQLModel):
    date_of_birth: date
    sex: Sex
    height_cm: float = Field(ge=120, le=240)
    current_weight_kg: float = Field(ge=35, le=250)
    primary_goal: NutritionGoal
    goal_intensity: GoalIntensity
    activity_level: ActivityLevel
    exercises: bool = False
    exercises_per_week: int | None = Field(default=None, ge=0, le=7)
    meals_per_day: int = Field(ge=2, le=6)
    selected_foods: list[str] = Field(default_factory=list)
    excluded_foods: list[str] = Field(default_factory=list)
    allergies: list[str] = Field(default_factory=list)
```

Note: if the local code uses `exercise_sessions_per_week` instead of `exercises_per_week`, keep the local name consistent throughout the rest of the implementation. The last screenshot showed `exercises_per_week`.

## Next Implementation Steps

Continue in `backend/app/models.py` manually.

Still needed:

1. `NutritionProfileUpdate`
2. `NutritionProfile`
3. `NutritionProfilePublic`
4. `User.nutrition_profile` relationship

Expected idea:

```python
class NutritionProfileUpdate(SQLModel):
    # Same fields as profile base, but optional.
    # Lists should be `list[str] | None = None` so updates do not clear lists accidentally.
```

Then:

```python
class NutritionProfile(NutritionProfileBase, table=True):
    # Database table with id, created_at, owner_id, owner relationship.
```

Then:

```python
class NutritionProfilePublic(NutritionProfileBase):
    # API output schema with id, owner_id, created_at.
```

## Do Not Do Yet

Do not start these until the model is reviewed:

- Alembic migration
- API routes
- CRUD helper functions
- frontend UI
- food catalog implementation
- validation service
- LangGraph agents

## Prompt For A New Chat

Paste this into a new chat:

```text
We are continuing `getsmced/ai-nutrition-assistant`. Read `docs/HANDOFF.md`, `docs/SESSION_LOG.md`, `docs/DECISIONS.md`, and `docs/PROFILE_QUESTIONNAIRE.md` first.

Important collaboration rule: do not edit backend/frontend/code files. The user writes code manually. You may only update docs if asked.

We are currently working through `backend/app/models.py`. The user has manually started adding `NutritionProfileBase` and the MVP Literal aliases. Continue by explaining and guiding the remaining model classes step by step: `NutritionProfileUpdate`, `NutritionProfile`, `NutritionProfilePublic`, and the `User.nutrition_profile` relationship.
```
