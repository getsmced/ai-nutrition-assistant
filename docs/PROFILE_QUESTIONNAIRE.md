# Nutrition Profile Questionnaire Design

This document defines the current MVP questionnaire and the validation logic that must run before meal-plan generation.

## Product Goal

The questionnaire should collect enough structured information to create a safe, realistic, personalized nutrition plan for a Greek-first MVP.

The UI should feel like a guided form with radio buttons, checkboxes, numeric inputs, and short optional text fields.

The Generate button must not blindly create a plan. It should first run validation and explain any blocking conflicts.

## Current MVP Scope

The first implementation should stay focused.

Included in the MVP profile:

- Basic body data
- Nutrition goal
- Goal intensity
- Daily activity level
- Simple exercise frequency
- Meals per day
- Selected foods
- Excluded foods
- Free-text allergies

Not included in the MVP profile yet:

- Broad dietary pattern selector such as Mediterranean, vegan, vegetarian, pescatarian
- Cooking skill
- Budget level
- Preferred cuisine style
- Detailed exercise type taxonomy
- Detailed medical flags

These may be added later after the profile, validation service, and calculation tools are working.

## Backend Values and Greek UI Labels

Backend values should stay as stable English keys. The Greek text belongs in the UI mapping.

Example:

```text
fat_loss -> Απώλεια λίπους
muscle_gain -> Αύξηση μυϊκής μάζας
maintenance -> Συντήρηση

mild -> Ήπια
moderate -> Μέτρια
intense -> Έντονη
```

This avoids Greek strings in database logic, validators, tests, and agents while still presenting the app fully in Greek.

## Planned Type Aliases

The first `models.py` aliases are:

```python
Sex = Literal["male", "female"]
NutritionGoal = Literal["fat_loss", "muscle_gain", "maintenance"]
GoalIntensity = Literal["mild", "moderate", "intense"]
ActivityLevel = Literal["sedentary", "light", "moderate", "very_active"]
```

`sedentary` should remain available because many users may have desk-based daily routines.

## MVP Profile Fields

The first `NutritionProfileBase` should include these concepts:

```text
date_of_birth
sex
height_cm
current_weight_kg
primary_goal
goal_intensity
activity_level
exercises
exercise_sessions_per_week
meals_per_day
selected_foods
excluded_foods
allergies
```

Required for profile creation:

```text
date_of_birth
sex
height_cm
current_weight_kg
primary_goal
goal_intensity
activity_level
meals_per_day
```

Optional or defaulted:

```text
exercises = False
exercise_sessions_per_week = None
selected_foods = []
excluded_foods = []
allergies = []
```

## Food Selection

Food choices should not be represented as a huge `Literal` type in `models.py`.

Instead, the profile should store stable food IDs:

```json
{
  "selected_foods": ["chicken_breast", "eggs", "rice"],
  "excluded_foods": ["pork", "tuna"]
}
```

The available choices should come from a separate food catalog, such as:

```text
backend/app/nutrition/food_catalog.py
```

or later from database tables such as:

```text
FoodCategory
FoodItem
```

The UI can show Greek labels while storing stable IDs.

Example:

```text
chicken_breast -> Στήθος κοτόπουλο
rice -> Ρύζι
eggs -> Αυγά
```

## Allergies

Allergies should be stored as free-text strings in the MVP:

```python
allergies: list[str]
```

Reason:

- The user may write allergies in natural language.
- The app can later normalize them through an agent or validation service.
- The normalized allergy terms can then become hard constraints for meal generation.

Example:

```json
{
  "allergies": ["φιστίκια", "λακτόζη", "γαρίδες"]
}
```

Later normalization could map:

```text
φιστίκια -> peanuts
λακτόζη -> milk/lactose-related
gaρίδες -> crustaceans
```

## User Flow

1. The user completes the questionnaire.
2. The user clicks Generate.
3. The backend validates the profile, goal, allergies, selected foods, and excluded foods.
4. If validation fails, the UI shows required corrections and no meal plan is generated.
5. If validation passes, deterministic tools calculate calorie and macro targets.
6. The meal-planning workflow creates a default plan.
7. Each meal can later offer three equivalent alternatives with similar calories and macros.

## Generate Validation

The Generate button must call a validation workflow before meal planning.

Validation result should return structured issues:

```json
{
  "can_generate": false,
  "issues": [
    {
      "code": "unrealistic_weight_loss_goal",
      "severity": "blocking",
      "message": "The requested target requires a weekly weight loss rate above the app safety threshold.",
      "suggested_actions": [
        "Extend the timeline",
        "Reduce the target weight loss"
      ]
    }
  ]
}
```

Issue severities:

- `blocking`: generation cannot continue.
- `warning`: generation can continue, but the user must see a caution.
- `info`: helpful guidance only.

## Meal Alternatives

After a valid plan is generated, each meal should support alternatives.

Initial MVP behavior:

- Generate one default plan.
- For any meal, the user can request three alternatives.
- Alternatives must target similar calories and macros.
- Alternatives must respect allergies, hard exclusions, selected foods, and excluded foods.

Example target passed to the meal-planning workflow:

```json
{
  "meal_type": "breakfast",
  "target_calories": 450,
  "target_protein_g": 30,
  "target_carbs_g": 45,
  "target_fat_g": 12,
  "forbidden_foods": ["peanuts", "milk"],
  "preferred_foods": ["oats", "eggs"]
}
```

## MVP Recommendation

Start with a single database-backed `NutritionProfile` model and a validation service.

Do not build full LangGraph orchestration before the profile, validators, calculation tools, and first food catalog exist.