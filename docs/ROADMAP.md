# AI Nutrition Assistant — Development Roadmap

## Phase 0: Project Foundation

- [x] Create the GitHub repository
- [x] Configure Git identity
- [x] Copy the FastAPI template
- [x] Protect the local `.env` file
- [x] Create and push the initial commit
- [x] Create the core documentation files
- [ ] Review the template structure
- [ ] Verify required development tools
- [ ] Run the original template locally

## Phase 1: Template Simplification

- [ ] Identify the backend components that will be retained
- [ ] Remove the React frontend
- [ ] Remove unused frontend packages and services
- [ ] Add an empty Streamlit service
- [ ] Update Docker Compose
- [ ] Verify communication between Streamlit and FastAPI
- [ ] Update the project README

## Phase 2: User Profile and Authentication

- [ ] Review the existing authentication flow
- [ ] Test user registration and login
- [ ] Design the nutrition profile schema
- [ ] Create the nutrition profile database model
- [ ] Create an Alembic migration
- [ ] Create profile API endpoints
- [ ] Add profile unit and integration tests
- [ ] Create the Streamlit onboarding pages

## Phase 3: Food Catalog and Preferences

- [ ] Design food categories
- [ ] Design the food and nutrient models
- [ ] Create the local curated food catalog
- [ ] Integrate a nutrition API
- [ ] Add dietary patterns
- [ ] Add allergies and food exclusions
- [ ] Create admin food-management endpoints
- [ ] Create the Streamlit food-selection interface

## Phase 4: Nutrition Calculation Engine

- [ ] Implement BMR calculation
- [ ] Implement TDEE calculation
- [ ] Implement calorie-target calculation
- [ ] Implement macronutrient-target calculation
- [ ] Implement portion conversions
- [ ] Implement meal and daily total calculations
- [ ] Write unit tests for every calculation
- [ ] Document formulas and assumptions

## Phase 5: Document Processing

- [ ] Design the extracted-value schema
- [ ] Implement temporary PDF and image upload
- [ ] Integrate OpenAI document extraction
- [ ] Add structured output validation
- [ ] Add confidence scores
- [ ] Add low-confidence user confirmation
- [ ] Implement temporary-file cleanup
- [ ] Create synthetic test documents

## Phase 6: LangGraph Meal-Planning Workflow

- [ ] Define the LangGraph state
- [ ] Implement document-extraction node
- [ ] Implement safety-rules node
- [ ] Implement nutrition-priorities node
- [ ] Implement food-selection node
- [ ] Implement target-calculation node
- [ ] Implement meal-plan generation node
- [ ] Implement deterministic validation node
- [ ] Implement correction loop
- [ ] Add workflow tests

## Phase 7: Meal Plans and Replacements

- [ ] Design meal-plan database models
- [ ] Generate weekly plans with two to six meals per day
- [ ] Display quantities, calories, and macronutrients
- [ ] Implement equivalent meal replacement
- [ ] Validate allergies and exclusions
- [ ] Store final meal-plan history
- [ ] Export plans to PDF

## Phase 8: Administration and Safety

- [ ] Add the administrator role
- [ ] Add food and recipe management
- [ ] Add approved-source management
- [ ] Add versioned safety rules
- [ ] Add AI-run audit information without health data
- [ ] Add warnings and medical limitations
- [ ] Review all privacy boundaries

## Phase 9: Portfolio Completion

- [ ] Improve the README
- [ ] Add architecture diagrams
- [ ] Add screenshots
- [ ] Record a short demonstration
- [ ] Add automated tests to GitHub Actions
- [ ] Add installation and usage instructions
- [ ] Document known limitations
- [ ] Prepare interview explanations
- [ ] Create a tagged MVP release