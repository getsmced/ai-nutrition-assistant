# Nutrition Profile Questionnaire Design

This document defines the first version of the user questionnaire and the validation logic that must run before meal-plan generation.

## Product Goal

The questionnaire should collect enough structured information to create a safe, realistic, personalized nutrition plan.

It should feel like a guided form with checkboxes, dropdowns, numeric inputs, and short optional text fields.

The Generate button must not blindly create a plan. It should first run validation and explain any blocking conflicts.

## User Flow

1. The user completes the questionnaire.
2. The user clicks Generate.
3. The backend validates the profile, goal, allergies, medical flags, and preference conflicts.
4. If validation fails, the UI shows required corrections and no meal plan is generated.
5. If validation passes, deterministic tools calculate calorie and macro targets.
6. The meal-planning workflow creates a default plan.
7. Each meal can later offer three equivalent alternatives with similar calories and macros.

## Sections

### 1. Basic Profile

Purpose: support BMR/TDEE and personalization.

Fields:

- Date of birth
- Sex
- Height in centimeters
- Current weight in kilograms
- Optional waist circumference
- Optional full name or display name

Example:

```text
Date of birth: 1995-04-12
Sex: male
Height: 178 cm
Weight: 86 kg
```

### 2. Goal

Purpose: define the direction and realism of the plan.

Fields:

- Primary goal
  - Fat loss
  - Muscle gain
  - Body recomposition
  - Maintenance
  - General health
  - Sports performance
- Target weight change in kilograms
- Target date or number of weeks
- Preferred pace
  - Conservative
  - Moderate
  - Aggressive but still safe

Validation examples:

- If requested weekly weight loss is too high, block generation.
- If the user wants muscle gain and aggressive fat loss at the same time, ask them to prioritize.

### 3. Dietary Pattern

Purpose: define broad food rules.

Checkboxes:

- Mediterranean
- Vegetarian
- Vegan
- Pescatarian
- High protein
- Lower carb
- No pork
- No alcohol
- Religious fasting pattern
- Other pattern

Conflict examples:

- Vegan conflicts with eggs, dairy, fish, poultry, and meat.
- Vegetarian conflicts with meat and fish unless the user selects pescatarian.

### 4. Allergies and Intolerances

Purpose: enforce non-negotiable safety constraints.

Initial checkbox list based on common EU allergen categories:

- Cereals containing gluten
- Crustaceans
- Eggs
- Fish
- Peanuts
- Soybeans
- Milk
- Nuts
- Celery
- Mustard
- Sesame
- Sulphur dioxide and sulphites
- Lupin
- Molluscs

Additional fields:

- Other allergy
- Intolerance notes
- Reaction severity, optional

Hard rule:

Allergy constraints must always override preferences and generated meals.

### 5. Food Preferences

Purpose: improve adherence and practicality.

Fields:

- Preferred protein foods
- Preferred carbohydrate foods
- Preferred fruits
- Preferred vegetables
- Favorite dishes
- Disliked foods
- Foods the user refuses to eat
- Preferred cuisine styles

Important distinction:

- Disliked food is a soft preference.
- Refused food is a hard exclusion.

### 6. Activity Profile

Purpose: estimate energy expenditure and adapt meal timing.

Fields:

- Daily activity level
  - Sedentary
  - Lightly active
  - Moderately active
  - Very active
- Exercise types
  - Resistance training
  - Running
  - Walking
  - Cycling
  - Team sports
  - HIIT/CrossFit
  - Yoga/Pilates
  - Other
- Sessions per week
- Minutes per session
- Intensity
  - Low
  - Moderate
  - High

Example:

```text
Daily activity: sedentary office work
Exercise: resistance training, 4 sessions/week, 60 minutes, moderate-high intensity
```

### 7. Daily Schedule and Practicality

Purpose: make plans realistic.

Fields:

- Wake-up time
- Sleep time
- Work/school schedule
- Meals per day
- Eats breakfast
- Can carry food to work
- Has fridge/microwave at work
- Cooking skill level
- Meal prep preference
- Maximum cooking time per meal
- Budget level

### 8. Medical and Safety Flags

Purpose: detect cases that require caution or professional guidance.

Checkboxes:

- Diabetes
- Hypertension
- Kidney disease
- Cardiovascular history
- Pregnancy or breastfeeding
- History of eating disorder
- Gastrointestinal condition
- Food allergy with severe reactions
- Medication that affects appetite or weight
- Currently followed by doctor or dietitian

Rules:

- Some flags should show warnings and continue with general guidance.
- Some combinations may block plan generation until the user confirms professional supervision.
- The app must not diagnose, prescribe, or claim to treat disease.

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
- Alternatives must respect allergies, hard exclusions, dietary pattern, and meal practicality.

Example target passed to the meal-planning workflow:

```json
{
  "meal_type": "breakfast",
  "target_calories": 450,
  "target_protein_g": 30,
  "target_carbs_g": 45,
  "target_fat_g": 12,
  "forbidden_foods": ["peanuts", "milk"],
  "preferred_foods": ["oats", "eggs"],
  "max_prep_time_minutes": 10
}
```

## MVP Recommendation

Start with a single database-backed Nutrition Profile model and a validation service.

Do not build full LangGraph orchestration before the profile, validators, and calculation tools exist.