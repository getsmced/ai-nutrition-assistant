# AI Nutrition Assistant — Project Context

## Project Goal

Build an AI-powered nutrition planning web application that creates personalized weekly meal plans based on:

- User body measurements and goals
- Physical activity and exercise
- Dietary preferences and allergies
- Selected and excluded foods
- Optional blood test or body composition documents

## Target Users

The MVP is designed for individual users who want a personalized weekly nutrition plan.

A nutritionist review workflow may be added in a future version.

## Core Technologies

- Python
- FastAPI backend
- Streamlit frontend
- PostgreSQL database
- SQLModel ORM
- LangGraph workflows
- OpenAI API
- Docker Compose
- Pytest
- Git and GitHub

## Main Architectural Principle

The language model must not perform nutritional calculations.

Calculations such as BMR, TDEE, calorie targets, macronutrients, and meal totals will be performed by deterministic and testable Python functions.

The AI model will be used for:

- Extracting structured information from uploaded documents
- Creating natural-language explanations
- Composing meal plans within validated constraints
- Suggesting equivalent meal replacements

## Safety Boundaries

The application:

- Does not provide medical diagnoses
- Does not prescribe medication or supplements
- Does not replace a doctor or registered nutrition professional
- Must warn users about uncertain or abnormal extracted values
- Must validate allergies and excluded foods before showing a plan
- Must not permanently store uploaded medical documents or extracted laboratory values in the MVP

## MVP Features

- Email and password authentication
- User nutrition profile
- Dietary preferences and allergies
- PDF or image document upload
- Structured extraction of document values
- User confirmation for low-confidence values
- Food group selection and exclusion
- Weekly meal-plan generation
- Two to six meals per day
- Calories and macronutrients per meal
- Equivalent meal replacement
- Previous meal-plan history
- PDF export
- Admin management for foods, recipes, safety rules, and AI content review

## Current Status

Completed:

- GitHub repository created
- Git identity configured
- FastAPI full-stack template copied
- Local repository connected to GitHub
- `.env` protected from Git
- `.env.example` created
- Initial commit pushed to `main`

Current milestone:

- Create the project documentation and development roadmap

Next milestone:

- Review and simplify the FastAPI template before writing application features