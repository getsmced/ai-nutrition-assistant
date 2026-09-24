# Development Session Log

This file records the progress, lessons, decisions, problems, and next steps from each development session.

---

## 2026-09-24 — Nutrition Profile Model Walkthrough and Handoff

### Completed

- Continued the code walkthrough of `backend/app/models.py` without assistant code edits.
- Reviewed the purpose of SQLModel models, API schemas, and database models.
- Explained why `Literal` is imported from Python `typing`, while `Field`, `Relationship`, and `SQLModel` come from `sqlmodel`.
- Explained the relationship between:
  - `UserCreate.password`,
  - `crud.py` hashing logic,
  - `User.hashed_password`,
  - and the database-stored password hash.
- Reviewed how `Relationship(back_populates=...)` links Python objects across database tables.
- Designed the first MVP `NutritionProfile` model shape.
- The user manually started adding the model code in `backend/app/models.py`.

### Code Written by User

The assistant did not edit backend code.

The user started adding the following concepts manually in `backend/app/models.py`:

- `date` import from `datetime`
- `Literal` import from `typing`
- Type aliases outside classes:

```python
Sex = Literal["male", "female"]
NutritionGoal = Literal["fat_loss", "muscle_gain", "maintenance"]
GoalIntensity = Literal["mild", "moderate", "intense"]
ActivityLevel = Literal["sedentary", "light", "moderate", "very_active"]
```

The user also started writing:

```python
class NutritionProfileBase(SQLModel):
```

with fields for basic body data, goal, activity, exercise, meal count, selected foods, excluded foods, and allergies.

### Decisions

- `Sex` will support only `"male"` and `"female"` for the first MVP, because the initial BMR formulas need one of those two branches.
- `NutritionGoal` will support:
  - `"fat_loss"`
  - `"muscle_gain"`
  - `"maintenance"`
- `GoalIntensity` will support:
  - `"mild"`
  - `"moderate"`
  - `"intense"`
- `ActivityLevel` should include `"sedentary"`, because many users may have mostly desk-based daily activity.
- `DietaryPattern` will not be used in the MVP model.
- Cooking skill and budget level will not be used in the MVP model.
- Food preferences will be represented as stable food IDs in `selected_foods` and `excluded_foods`.
- Food choices should come from a separate food catalog, not from `Literal` values in `models.py`.
- Allergies will be stored as `list[str]`, because the user should be able to write free text and the app/agent can later normalize it.
- Exercise will stay simple for MVP: whether the user exercises and how many sessions per week.

### Learned

- `Literal` is best for small fixed sets such as sex, goal, intensity, and activity level.
- Large domain lists, such as foods, should not be hard-coded as `Literal` types in `models.py`.
- Greek labels should appear in the UI, while backend values should remain stable English keys.
- Required fields do not use `| None` and do not use `default=None`.
- Numeric required fields with limits use `Field`, for example:

```python
height_cm: float = Field(ge=120, le=240)
```

- `Literal` should not wrap `Field`; `Literal` is for fixed values, while `Field` is for validation constraints and metadata.

### Next Steps

- Finish the remaining `NutritionProfile` classes in `models.py` manually:
  - `NutritionProfileUpdate`
  - `NutritionProfile`
  - `NutritionProfilePublic`
- Add the `User.nutrition_profile` relationship manually.
- Review the finished `models.py` with the assistant before moving on.
- After the model is correct, discuss migrations and routes, but the assistant must not modify code.

---

## 2026-09-22 — Agentic Nutrition Planning Design

### Completed

- Reviewed the existing project documentation and confirmed the project is still in Phase 0 / early Phase 1 planning.
- Discussed the product direction for a questionnaire-driven nutrition planning experience.
- Decided that the app should use a guarded multi-agent architecture instead of a simple diet chatbot.
- Documented the architecture decision in `docs/DECISIONS.md`.
- Created `docs/PROFILE_QUESTIONNAIRE.md` to describe the first questionnaire, validation flow, and meal-alternative concept.
- Clarified the Generate flow:
  - validate profile and goals first,
  - block generation when conflicts or unsafe goals exist,
  - calculate targets deterministically,
  - generate a default plan only after validation passes,
  - offer equivalent meal alternatives after plan generation.

### Decisions

- The assistant may update documentation files in `docs/` to record progress and design decisions.
- The assistant must not modify backend, frontend, infrastructure, migration, or other real code files.
- The user will write implementation code manually, with step-by-step explanation and guidance from the assistant.
- Hard safety rules, allergy rules, unrealistic-goal checks, and medical flags must be enforced by deterministic code, not by prompt wording alone.
- The language model may help with conversation, explanation, meal ideas, and alternatives, but not with final authority over safety or nutrition calculations.

### Learned

- Checkbox-style UI inputs should be treated as structured constraints, not just user preferences.
- The app should separate hard constraints from soft preferences.
- The Generate button should mean `Validate -> Calculate -> Generate`, not blind plan generation.
- Giving three alternatives for every meal immediately may overwhelm users; a better MVP is one default plan with a replacement action that returns three equivalent options for a selected meal.

### Next Steps

- Read and explain `backend/app/models.py` without editing it.
- Design the first `NutritionProfile` model together before the user writes code.
- Decide which fields belong in the MVP profile and which should wait.
- Design the validation result shape before implementing validators.

---

## 2026-09-21 — Repository and Project Foundation

### Completed

- Created the public GitHub repository `ai-nutrition-assistant`
- Configured the Git author name and email
- Cloned the empty GitHub repository locally
- Downloaded the official Full Stack FastAPI Template
- Copied the template files without copying its Git history
- Connected the local repository to the correct GitHub remote
- Created `.env.example`
- Added `.env` protection rules to `.gitignore`
- Verified that `.env` was not staged
- Created the initial Git commit
- Pushed the `main` branch to GitHub
- Started the project documentation

### Learned

- The difference between a local and remote repository
- The purpose of `git clone`
- The meaning of `origin`
- The difference between `fetch` and `push`
- The meaning of untracked and staged files
- The purpose of `git add`
- The purpose of a Git commit
- The purpose of `.gitignore`
- The difference between `.env` and `.env.example`
- Why secrets must never be committed to a public repository
- Why the template Git history was not copied into this project

### Problems Resolved

#### Incorrect GitHub username in clone URL

The first suggested clone URL contained a typo in the GitHub username.

Correct repository URL:

```text
https://github.com/getsmced/ai-nutrition-assistant.git
```
