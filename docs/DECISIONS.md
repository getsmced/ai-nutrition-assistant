# AI Nutrition Assistant — Architecture Decisions

This file records product and technical decisions that should guide implementation.

---

## 2026-09-24 — MVP Nutrition Profile Modeling Scope

### Decision

The first nutrition profile model will be intentionally small and focused.

The MVP profile should collect:

- Date of birth
- Sex
- Height
- Current weight
- Primary nutrition goal
- Goal intensity
- Daily activity level
- Whether the user exercises
- Exercise sessions per week
- Meals per day
- Selected foods
- Excluded foods
- Free-text allergies

### Type Aliases

The first fixed-value aliases are:

```python
Sex = Literal["male", "female"]
NutritionGoal = Literal["fat_loss", "muscle_gain", "maintenance"]
GoalIntensity = Literal["mild", "moderate", "intense"]
ActivityLevel = Literal["sedentary", "light", "moderate", "very_active"]
```

### Postponed

Do not add these to the MVP model yet:

- `DietaryPattern`
- fixed `Allergen` literal lists
- detailed `ExerciseType`
- `CookingSkill`
- `BudgetLevel`

### Rationale

The first profile should support the earliest useful calculation and planning workflow without becoming a large form too early.

Foods should be represented as stable IDs in lists such as `selected_foods` and `excluded_foods`. The available food choices belong in a separate food catalog, not in huge `Literal` definitions inside `models.py`.

Allergies should be free-text strings for now because users may enter natural Greek descriptions. Later, a validation or agent step can normalize those strings into internal allergen and forbidden-food concepts.

---

## 2026-09-24 — Documentation-Only Assistant Rule

### Decision

The assistant may only edit documentation files in the `docs/` directory, and only to record project progress, decisions, handoff notes, or explanations requested by the user.

The assistant must not edit:

- backend code,
- frontend code,
- migrations,
- infrastructure files,
- dependency files,
- generated files,
- configuration files outside `docs/`.

### Rationale

The user wants to write all implementation code manually as a learning exercise. The assistant's role is to explain, guide, review snippets/screenshots, and keep documentation up to date.

---

## 2026-09-22 — Build a Guarded Multi-Agent Nutrition Planning System

### Decision

The project will not be a simple chatbot that directly generates diet plans.

It will be a guarded nutrition planning system that combines:

- Structured user profile data
- Deterministic Python tools for calculations
- Hard safety rules and conflict validation
- Curated evidence and guideline notes
- Multi-agent orchestration for conversation, planning, explanation, and validation

The language model may help with natural-language explanations, structured conversation, meal ideas, and equivalent meal alternatives, but it must not be the authority for calories, macronutrients, allergies, unsafe goals, or medical safety boundaries.

### Rationale

Nutrition planning involves user safety, allergies, unrealistic goals, and medical-adjacent information. A free-form LLM response is not reliable enough for these responsibilities.

The safer architecture is:

1. Collect structured data through a questionnaire.
2. Validate hard constraints before generation.
3. Calculate targets with deterministic code.
4. Retrieve relevant guideline notes from curated project knowledge.
5. Generate meal-plan candidates within validated constraints.
6. Validate generated meals before presenting them to the user.

### Agent Roles

Initial planned agents:

- Profile Agent: collects and normalizes user answers.
- Safety Agent: detects blocking conflicts, medical flags, and unrealistic goals.
- Evidence Agent: retrieves relevant curated guideline notes.
- Meal Planning Agent: proposes meals within calorie, macro, preference, and safety constraints.
- Validation Agent: checks generated meals against allergies, exclusions, calories, and macro targets.

### Hard Rules

Hard rules must be enforced by code, not by prompt wording alone.

Examples:

- Food allergies cannot be violated.
- Excluded foods cannot appear in generated meals.
- Unrealistic weight-loss goals must block generation until changed.
- Medical red flags must trigger an appropriate warning or stop condition.
- The app must not diagnose disease, prescribe medication, or replace clinical care.

### Soft Preferences

Soft preferences should guide planning but can be relaxed if needed.

Examples:

- Preferred cuisine
- Favorite foods
- Budget level
- Meal prep time
- Number of meals per day
- Repeated meals versus variety

### Evidence Sources

The MVP should start with curated notes from reliable public sources, including:

- WHO physical activity guidelines
- CDC or NHLBI weight-loss guidance
- EU food allergen information
- Project-specific safety rules

The source notes should be stored in the repository before being used by agents. Retrieval can start with simple keyword matching and later evolve into embeddings/RAG.

### Generation UX

The Generate action means:

1. Validate profile and goal.
2. If there are blocking issues, do not generate a plan.
3. Explain what must change and offer realistic alternatives.
4. If the profile passes validation, calculate targets and generate the meal plan.
5. Present a default plan, with equivalent alternatives available for each meal.

For MVP, avoid overwhelming the user with too many alternatives at once. Prefer one default plan and a "replace meal" action that returns three equivalent options.