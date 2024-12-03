# HW-10 Event Manager Company: Software QA Analyst/Developer Onboarding Assignment

Welcome to the Event Manager Company! As a newly hired Software QA Analyst/Developer and a student in software engineering, you are embarking on an exciting journey to contribute to our project aimed at developing a secure, robust REST API that supports JWT token-based OAuth2 authentication. This API serves as the backbone of our user management system and will eventually expand to include features for event management and registration.

## Setup and Preliminary Steps
1. Fork the Project Repository: Fork the project repository to my own GitHub account. 

2. Clone the Forked Repository: Clone the forked repository to our local machine using the git clone command. This creates a local copy of the repository on our computer, enabling we  make changes and run the project locally.
- git clone git@github.com:nisha2110/HW-10_event_manager.git

3. Verify the Project Setup: Follow the steps in the instructor video to set up the project using Docker. Docker allows our to package the application with all its dependencies into a standardized unit called a container. Verify that you can access the API documentation at http://localhost/docs and the database using PGAdmin at http://localhost:5050.

## Commands
- docker compose up --build
- docker compose exec fastapi pytest
- docker compose exec fastapi pytest tests/test_services/test_user_service.py::test_list_users
- Need to apply database migrationss: docker compose exec fastapi alembic upgrade head
- Creating database migration: docker compose exec fastapi alembic revision --autogenerate -m 'added admin'

## Issues to Address:
1. Validation Error :
 - The errors in tests indicate mismatches between the fields in test data (user_base_data, user_create_data, etc.) and the actual schema definitions (UserBase, UserCreate, UserUpdate, etc.).
 KeyError: Indicates that the expected keys (nickname, first_name, etc.) are missing from the test data.
 ValidationError: Indicates that the input data does not match the expected schema.

- Fix Error:
- change file https://github.com/nisha2110/HW-10_event_manager_final/blob/main/tests/test_schemas/test_user_schemas.py
- Link https://github.com/nisha2110/HW-10_event_manager_final/blob/main/1-1-validation.PNG

