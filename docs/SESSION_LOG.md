# Development Session Log

This file records the progress, lessons, decisions, problems, and next steps from each development session.

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
