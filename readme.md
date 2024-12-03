# Enhancements and Issue Resolutions in the User Management API: Resolved Issues and Enhancements

## Table of Contents
1. [Missing Required Data in User Fixtures](#1-missing-required-data-in-user-fixtures)
2. [Implemented User ID Validation Using UUID](#2-implemented-user-id-validation-using-uuid)
3. [Resolved Validation Error for Login Request](#3-resolved-validation-error-for-login-request)
4. [Fixture Failed SMTP Connection](#4-fixture-failed-smtp-connection)
5. [Implemented Email Validation](#5-implemented-email-validation)
6. [Cleaned Up User-Related Files](#6-cleaned-up-user-related-files)
7. [Build and Publish Image to DockerHub](#7-build-and-publish-image-to-dockerhub)

---

### 1. Missing Required Data in User Fixtures

**Issue:** The `conftest.py` fixtures lacked required fields, causing tests like `test_user_base_valid` to fail.

**Resolution:**
- Added the `nickname` field to the base user fixture.
- Incorporated the `first_name` field in the `user_update_data` fixture.
- Ensured all fixtures align with test requirements and API expectations.

---

### 2. Implemented User ID Validation Using UUID

**Issue:** Tests failed because the `id` field in the UserResponse schema required a UUID format, but the fixture lacked it.

**Resolution:**
- Updated the `conftest.py` fixture to generate UUID values for the `id` field.
- Ensured all relevant tests adhere to schema requirements for the `id` field.

---

### 3. Resolved Validation Error for Login Request

**Issue:** Tests for LoginRequest validation failed due to a missing `email` field in the fixture.

**Resolution:**
- Added the `email` field to the `login_request_data` fixture.
- Ensured the fixture aligns with API validation requirements, allowing tests to pass successfully.

---

### 4. Fixture Failed SMTP Connection

**Issue:** Email-related tests failed due to improper SMTP configuration.

**Resolution:**
- Configured Mailtrap credentials in the test environment.
- Verified SMTP connection to ensure successful execution of email-related tests.

---

### 5. Implemented Email Validation

**Issue:** Email fields lacked proper validation, allowing invalid formats to be accepted.

**Resolution:**
- Added regex-based validation to enforce standard email formats.
- Wrote comprehensive test cases to handle various email scenarios, including edge cases.

---

### 6. Cleaned Up User-Related Files

**Issue:** User-related files contained unused variables, duplicate imports, and redundant fields.

**Resolution:**
- Removed unused variables and reorganized imports for better clarity.
- Fixed duplicate field issues in `userListResponse`.
- Addressed duplicate test names to prevent conflicts and enhance maintainability.
- Improved error handling for edge cases.

---

### 7. Build and Publish Image to DockerHub

**Issue:** The CI/CD pipeline needed updates to publish the Docker image to DockerHub.

**Resolution:**
- Updated the DockerHub repository to point to a personal profile for improved management.
- Configured GitHub Actions to:
  - Include environment variables for email service during pytest.
  - Build and publish Docker images upon successful test execution.
- Addressed vulnerabilities in dependencies (e.g., Gunicorn) to ensure enhanced security and stability.
- Enhanced test fixture files to align with updated requirements and improve accuracy.

---
# Test Coverage and Docker Profile

### Test Coverage Report
![image](https://github.com/saisrinivas194/event_manager/blob/13-build-and-publish-image-to-dockerhub/Screenshot%202024-12-02%20at%2010.23.44%E2%80%AFPM.png)
*Detailed test coverage report showing module-wise coverage metrics and overall coverage percentage*

### Docker Profile
You can find the Docker image for the Event Management project on Docker Hub:  
[Event Management Docker Image](https://hub.docker.com/repository/docker/saisrinivas194/event_management/general)
![image](https://github.com/saisrinivas194/event_manager/blob/13-build-and-publish-image-to-dockerhub/Screenshot%202024-12-02%20at%2010.26.11%E2%80%AFPM.png)
*Docker profile showing container configurations and resource usage*

## Key Learnings

- **Testing Discipline:** Regularly running tests after each change helped in identifying and resolving issues early in the development process.
- **Code Quality Tools:** Using linters and automated checks ensured adherence to best practices and enhanced overall code quality.
- **Thorough Documentation:** Regularly referencing project requirements and documentation clarified expectations and guided development effectively.
